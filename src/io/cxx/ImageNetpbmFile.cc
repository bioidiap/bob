/**
 * @file io/cxx/ImageNetpbmFile.cc
 * @date Tue Oct 9 18:13:00 2012 +0200
 * @author Laurent El Shafey <laurent.el-shafey@idiap.ch>
 *
 * @brief Implements an image format reader/writer using libnetpbm.
 * This codec is only able to work with 2D and 3D input.
 *
 * Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3 of the License.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <boost/filesystem.hpp>
#include <boost/shared_array.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/make_shared.hpp>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include <string>

#include <bob/io/CodecRegistry.h>

#include "pnmio.h"

typedef unsigned long sample;

struct pam {
/* This structure describes an open PAM image file.  It consists
   entirely of information that belongs in the header of a PAM image
   and filesystem information.  It does not contain any state
   information about the processing of that image.

   This is not considered to be an opaque object.  The user of Netbpm
   libraries is free to access and set any of these fields whenever
   appropriate.  The structure exists to make coding of function calls
   easy.
*/

    /* 'size' and 'len' are necessary in order to provide forward and
       backward compatibility between library functions and calling programs
       as this structure grows.
       */
    unsigned int size;
        /* The storage size of this entire structure, in bytes */
    unsigned int len;
        /* The length, in bytes, of the information in this structure.
           The information starts in the first byte and is contiguous.
           This cannot be greater than 'size'
           */
    FILE *file;
    int format;
        /* The format code of the raw image.  This is PAM_FORMAT
           unless the PAM image is really a view of a PBM, PGM, or PPM
           image.  Then it's PBM_FORMAT, RPBM_FORMAT, etc.
           */
    unsigned int plainformat;
        /* Logical:  the format above is a plain (text) format as opposed
           to a raw (binary) format.  This is entirely redundant with the
           'format' member and exists as a separate member only for
           computational speed.
        */
    int height;  /* Height of image in rows */
    int width;
        /* Width of image in number of columns (tuples per row) */
    unsigned int depth;
        /* Depth of image (number of samples in each tuple). */
    sample maxval;  /* Maximum defined value for a sample */
    unsigned int bytes_per_sample;
        /* Number of bytes used to represent each sample in the image file.
           Note that this is strictly a function of 'maxval'.  It is in a
           a separate member for computational speed.
           */
    char tuple_type[256];
        /* The tuple type string from the image header.  Netpbm does
           not define any values for this except the following, which are
           used for a PAM image which is really a view of a PBM, PGM,
           or PPM image:  PAM_PBM_TUPLETYPE, PAM_PGM_TUPLETYPE,
           PAM_PPM_TUPLETYPE.
           */
};


/* File open/close that handles "-" as stdin/stdout and checks errors. */

FILE*
pm_openr(const char * const name) {
    FILE* f;

    if (strcmp(name, "-") == 0)
        f = stdin;
    else {
#ifndef VMS
        f = fopen(name, "rb");
#else
        f = fopen (name, "r", "ctx=stm");
#endif
    }
    return f;
}

FILE*
pm_openw(const char * const name) {
    FILE* f;

    if (strcmp(name, "-") == 0)
        f = stdout;
    else {
#ifndef VMS
        f = fopen(name, "wb");
#else
        f = fopen (name, "w", "mbc=32", "mbf=2");  /* set buffer factors */
#endif
    }
    return f;
}

void
pm_close(FILE * const f) {
  fflush(f);
  if (f != stdin) fclose( f );
}

static boost::shared_ptr<std::FILE> make_cfile(const char *filename, const char *flags)
{
  std::FILE* fp;
  if(strcmp(flags, "r") == 0)
    fp = pm_openr(filename);
  else // write
    fp = pm_openw(filename);
  if(fp == 0) {
    boost::format m("cannot open file `%s'");
    m % filename;
    throw std::runtime_error(m.str());
  }
  return boost::shared_ptr<std::FILE>(fp, pm_close);
}

static void pnm_readpaminit(FILE *file, struct pam * const pamP, const int size) {
  int pnm_type=0;
  int x_dim=256, y_dim=256;
  int enable_ascii=1, img_colors=1;
  int read_err;

  pamP->file = file;
  pnm_type = get_pnm_type(pamP->file);
  rewind(pamP->file);
  pamP->format = pnm_type;

  /* Read the image file header (the input file has been rewinded). */
  if ((pnm_type == PBM_ASCII) || (pnm_type == PBM_BINARY)) {
    read_err = read_pbm_header(file, &x_dim, &y_dim, &enable_ascii);
    pamP->bytes_per_sample = 1;
  } else if ((pnm_type == PGM_ASCII) || (pnm_type == PGM_BINARY)) {
    read_err = read_pgm_header(file, &x_dim, &y_dim, &img_colors, &enable_ascii);
    if (img_colors >> 8 == 0)       pamP->bytes_per_sample = 1;
    else if (img_colors >> 16 == 0) pamP->bytes_per_sample = 2;
  } else if ((pnm_type == PPM_ASCII) || (pnm_type == PPM_BINARY)) {
    read_err = read_ppm_header(file, &x_dim, &y_dim, &img_colors, &enable_ascii);
    if (img_colors >> 8 == 0)       pamP->bytes_per_sample = 1;
    else if (img_colors >> 16 == 0) pamP->bytes_per_sample = 2;
  } else {
    boost::format m("pnm_readpaminit(): Unknown PNM/PFM image format.");
    throw std::runtime_error(m.str());
  }

  if (read_err != 0) {
    boost::format m("pnm_readpaminit(): Something went wrong when reading the image file.");
    throw std::runtime_error(m.str());
  }

  /* Perform operations. */
  if ((pnm_type == PPM_ASCII) || (pnm_type == PPM_BINARY)) {
    pamP->depth = 3;
  } else {
    pamP->depth = 1;
  }
  pamP->width = x_dim;
  pamP->height = y_dim;
  pamP->plainformat = enable_ascii;
  pamP->maxval = img_colors;

}

static int * pnm_allocpam(struct pam * const pamP) {
  int *img_data;
  /* Perform operations. */
  if ((pamP->format == PPM_ASCII) || (pamP->format == PPM_BINARY)) {
    img_data = (int *) malloc((3 * pamP->width * pamP->height) * sizeof(int));
  } else {
    img_data = (int *) malloc((pamP->width * pamP->height) * sizeof(int));
  }
  return (img_data);
}

static void pnm_readpam(struct pam * const pamP, int *img_data) {
  int read_err=1;

  /* Read the image data. */
  if ((pamP->format == PBM_ASCII) || (pamP->format == PBM_BINARY)) {
    read_err = read_pbm_data(pamP->file, img_data, pamP->width * pamP->height, pamP->plainformat, pamP->width);
  } else if ((pamP->format == PGM_ASCII) || (pamP->format == PGM_BINARY)) {
    read_err = read_pgm_data(pamP->file, img_data, pamP->width * pamP->height, pamP->plainformat, pamP->bytes_per_sample);
  } else if ((pamP->format == PPM_ASCII) || (pamP->format == PPM_BINARY)) {
    read_err = read_ppm_data(pamP->file, img_data, 3 * pamP->width * pamP->height, pamP->plainformat, pamP->bytes_per_sample);
  }

  if (read_err != 0) {
    boost::format m("pnm_readpam(): Something went wrong when reading the image file.");
    throw std::runtime_error(m.str());
  }
}

static void pnm_writepam(struct pam * const pamP, int *img_data) {
  int write_err=1;

  /* Write the output image file. */
  if ((pamP->format == PBM_ASCII) || (pamP->format == PBM_BINARY)) {
    write_err = write_pbm_file(pamP->file, img_data,
      pamP->width, pamP->height, 1, 1, 32, pamP->plainformat
    );
  } else if ((pamP->format == PGM_ASCII) || (pamP->format == PGM_BINARY)) {
    write_err = write_pgm_file(pamP->file, img_data,
      pamP->width, pamP->height, 1, 1, pamP->maxval, 16, pamP->plainformat,
      pamP->bytes_per_sample
    );
  } else if ((pamP->format == PPM_ASCII) || (pamP->format == PPM_BINARY)) {
    write_err = write_ppm_file(pamP->file, img_data,
      pamP->width, pamP->height, 1, 1, pamP->maxval, pamP->plainformat,
      pamP->bytes_per_sample
    );
  }

  if (write_err != 0) {
    boost::format m("pnm_writepam(): Something went wrong when writing the image file.");
    throw std::runtime_error(m.str());
  }
}

/**
 * LOADING
 */
static void im_peek(const std::string& path, bob::core::array::typeinfo& info) {

  struct pam in_pam;
  boost::shared_ptr<std::FILE> in_file = make_cfile(path.c_str(), "r");
  pnm_readpaminit(in_file.get(), &in_pam, sizeof(struct pam));

  if( in_pam.depth != 1 && in_pam.depth != 3)
  {
    boost::format m("unsupported number of planes (%d) when reading file. Image depth must be 1 or 3.");
    m % in_pam.depth;
    throw std::runtime_error(m.str());
  }

  info.nd = (in_pam.depth == 1? 2 : 3);
  if(info.nd == 2)
  {
    info.shape[0] = in_pam.height;
    info.shape[1] = in_pam.width;
  }
  else
  {
    info.shape[0] = 3;
    info.shape[1] = in_pam.height;
    info.shape[2] = in_pam.width;
  }
  info.update_strides();

  // Set depth
  if (in_pam.bytes_per_sample == 1) info.dtype = bob::core::array::t_uint8;
  else if (in_pam.bytes_per_sample == 2) info.dtype = bob::core::array::t_uint16;
  else {
    boost::format m("unsupported image depth (%d bytes per samples) when reading file");
    m % in_pam.bytes_per_sample;
    throw std::runtime_error(m.str());
  }
}

template <typename T> static
void im_load_gray(struct pam *in_pam, bob::core::array::interface& b) {
  const bob::core::array::typeinfo& info = b.type();
  int c=0;

  T *element = static_cast<T*>(b.ptr());
  int *img_data = pnm_allocpam(in_pam);
  pnm_readpam(in_pam, img_data);
  for(size_t y=0; y<info.shape[0]; ++y)
  {
    for(size_t x=0; x<info.shape[1]; ++x)
    {
      *element = img_data[c];
      ++element;
      c++;
    }
  }
  free(img_data);
}

template <typename T> static
void im_load_color(struct pam *in_pam, bob::core::array::interface& b) {
  const bob::io::base::array::typeinfo& info = b.type();
  int c=0;

  long unsigned int frame_size = info.shape[2] * info.shape[1];
  T *element_r = static_cast<T*>(b.ptr());
  T *element_g = element_r+frame_size;
  T *element_b = element_g+frame_size;

  int *img_data = pnm_allocpam(in_pam);
  pnm_readpam(in_pam, img_data);
  for(size_t y=0; y<info.shape[1]; ++y)
  {
    for(size_t x=0; x<info.shape[2]; ++x)
    {
      element_r[y*info.shape[2] + x] = img_data[c+0];
      element_g[y*info.shape[2] + x] = img_data[c+1];
      element_b[y*info.shape[2] + x] = img_data[c+2];
      c = c + 3;
    }
  }
  free(img_data);
}

static void im_load (const std::string& filename, bob::core::array::interface& b) {

  struct pam in_pam;
  boost::shared_ptr<std::FILE> in_file = make_cfile(filename.c_str(), "r");
  pnm_readpaminit(in_file.get(), &in_pam, sizeof(struct pam));

  const bob::core::array::typeinfo& info = b.type();

  if (info.dtype == bob::core::array::t_uint8) {
    if(info.nd == 2) im_load_gray<uint8_t>(&in_pam, b);
    else if( info.nd == 3) im_load_color<uint8_t>(&in_pam, b);
    else {
      boost::format m("(netpbm) unsupported image type found in file `%s': %s");
      m % filename % info.str();
      throw std::runtime_error(m.str());
    }
  }

  else if (info.dtype == bob::core::array::t_uint16) {
    if(info.nd == 2) im_load_gray<uint16_t>(&in_pam, b);
    else if( info.nd == 3) im_load_color<uint16_t>(&in_pam, b);
    else {
      boost::format m("(netpbm) unsupported image type found in file `%s': %s");
      m % filename % info.str();
      throw std::runtime_error(m.str());
    }
  }

  else {
    boost::format m("(netpbm) unsupported image type found in file `%s': %s");
    m % filename % info.str();
    throw std::runtime_error(m.str());
  }
}

/**
 * SAVING
 */
template <typename T>
static void im_save_gray(const bob::core::array::interface& b, struct pam *out_pam) {
  const bob::core::array::typeinfo& info = b.type();
  int c=0;

  const T *element = static_cast<const T*>(b.ptr());

  int *img_data = pnm_allocpam(out_pam);
  for(size_t y=0; y<info.shape[0]; ++y)
  {
    for(size_t x=0; x<info.shape[1]; ++x)
    {
      img_data[c] = *element;
      ++element;
      c++;
    }
  }
  pnm_writepam(out_pam, img_data);
  free(img_data);
}


template <typename T>
static void im_save_color(const bob::core::array::interface& b, struct pam *out_pam) {
  const bob::core::array::typeinfo& info = b.type();
  int c=0;

  long unsigned int frame_size = info.shape[2] * info.shape[1];
  const T *element_r = static_cast<const T*>(b.ptr());
  const T *element_g = element_r + frame_size;
  const T *element_b = element_g + frame_size;

  int *img_data = pnm_allocpam(out_pam);
  for(size_t y=0; y<info.shape[1]; ++y)
  {
    for(size_t x=0; x<info.shape[2]; ++x)
    {
      img_data[c+0] = element_r[y*info.shape[2] + x];
      img_data[c+1] = element_g[y*info.shape[2] + x];
      img_data[c+2] = element_b[y*info.shape[2] + x];
      c += 3;
    }
  }
  pnm_writepam(out_pam, img_data);
  free(img_data);
}

static void im_save (const std::string& filename, const bob::core::array::interface& array) {

  const bob::core::array::typeinfo& info = array.type();

  struct pam out_pam;
  boost::shared_ptr<std::FILE> out_file = make_cfile(filename.c_str(), "w");

  std::string ext = boost::filesystem::path(filename).extension().c_str();
  boost::algorithm::to_lower(ext);

  // Sets the parameters of the pam structure according to the bca::interface properties
  out_pam.size = sizeof(out_pam);
  out_pam.len = out_pam.size;
  out_pam.file = out_file.get();
  out_pam.plainformat = 0; // writes in binary
  out_pam.height = (info.nd == 2 ? info.shape[0] : info.shape[1]);
  out_pam.width = (info.nd == 2 ? info.shape[1] : info.shape[2]);
  out_pam.depth = (info.nd == 2 ? 1 : 3);
  out_pam.maxval = (info.dtype == bob::core::array::t_uint8 ? 255 : 65535);
  out_pam.bytes_per_sample = (info.dtype == bob::core::array::t_uint8 ? 1 : 2);
  if( ext.compare(".pbm") == 0)
  {
    out_pam.maxval = 1;
    out_pam.format = PBM_BINARY;
  }
  else if( ext.compare(".pgm") == 0)
  {
    out_pam.format = PGM_BINARY;
  }
  else
  {
    out_pam.format = PPM_BINARY;
  }

  if(out_pam.depth == 3 && ext.compare(".ppm")) {
    throw std::runtime_error("cannot save a color image into a file of this type.");
  }

  // Writes content
  if(info.dtype == bob::core::array::t_uint8) {

    if(info.nd == 2) im_save_gray<uint8_t>(array, &out_pam);
    else if(info.nd == 3) {
      if(info.shape[0] != 3) throw std::runtime_error("color image does not have 3 planes on 1st. dimension");
      im_save_color<uint8_t>(array, &out_pam);
    }
    else {
      boost::format m("(netpbm) cannot write object of type `%s' to file `%s'");
      m % info.str() % filename;
      throw std::runtime_error(m.str());
    }

  }

  else if(info.dtype == bob::core::array::t_uint16) {

    if(info.nd == 2) im_save_gray<uint16_t>(array, &out_pam);
    else if(info.nd == 3) {
      if(info.shape[0] != 3) throw std::runtime_error("color image does not have 3 planes on 1st. dimension");
      im_save_color<uint16_t>(array, &out_pam);
    }
    else {
      boost::format m("(netpbm) cannot write object of type `%s' to file `%s'");
      m % info.str() % filename;
      throw std::runtime_error(m.str());
    }

  }

  else {
    boost::format m("(netpbm) cannot write object of type `%s' to file `%s'");
    m % info.str() % filename;
    throw std::runtime_error(m.str());
  }
}


/**
 * NetPBM class
*/


class ImageNetpbmFile: public bob::io::File {

  public: //api

    ImageNetpbmFile(const std::string& path, char mode):
      m_filename(path),
      m_newfile(true) {

        //checks if file exists
        if (mode == 'r' && !boost::filesystem::exists(path)) {
          boost::format m("file '%s' is not readable");
          m % path;
          throw std::runtime_error(m.str());
        }

        if (mode == 'r' || (mode == 'a' && boost::filesystem::exists(path))) {
          {
            im_peek(path, m_type);
            m_length = 1;
            m_newfile = false;
          }
        }
        else {
          m_length = 0;
          m_newfile = true;
        }
      }

    virtual ~ImageNetpbmFile() { }

    virtual const std::string& filename() const {
      return m_filename;
    }

    virtual const bob::core::array::typeinfo& type_all() const {
      return m_type;
    }

    virtual const bob::core::array::typeinfo& type() const {
      return m_type;
    }

    virtual size_t size() const {
      return m_length;
    }

    virtual const std::string& name() const {
      return s_codecname;
    }

    virtual void read_all(bob::core::array::interface& buffer) {
      read(buffer, 0); ///we only have 1 image in an image file anyways
    }

    virtual void read(bob::core::array::interface& buffer, size_t index) {

      if (m_newfile)
        throw std::runtime_error("uninitialized image file cannot be read");

      if (!buffer.type().is_compatible(m_type)) buffer.set(m_type);

      if (index != 0)
        throw std::runtime_error("cannot read image with index > 0 -- there is only one image in an image file");

      if(!buffer.type().is_compatible(m_type)) buffer.set(m_type);
      im_load(m_filename, buffer);
    }

    virtual size_t append (const bob::core::array::interface& buffer) {
      if (m_newfile) {
        im_save(m_filename, buffer);
        m_type = buffer.type();
        m_newfile = false;
        m_length = 1;
        return 0;
      }

      throw std::runtime_error("image files only accept a single array");
    }

    virtual void write (const bob::core::array::interface& buffer) {
      //overwriting position 0 should always work
      if (m_newfile) {
        append(buffer);
        return;
      }

      throw std::runtime_error("image files only accept a single array");
    }

  private: //representation
    std::string m_filename;
    bool m_newfile;
    bob::core::array::typeinfo m_type;
    size_t m_length;

    static std::string s_codecname;

};

std::string ImageNetpbmFile::s_codecname = "bob.image_netpbm";

/**
 * From this point onwards we have the registration procedure. If you are
 * looking at this file for a coding example, just follow the procedure bellow,
 * minus local modifications you may need to apply.
 */

/**
 * This defines the factory method F that can create codecs of this type.
 *
 * Here are the meanings of the mode flag that should be respected by your
 * factory implementation:
 *
 * 'r': opens for reading only - no modifications can occur; it is an
 *      error to open a file that does not exist for read-only operations.
 * 'w': opens for reading and writing, but truncates the file if it
 *      exists; it is not an error to open files that do not exist with
 *      this flag.
 * 'a': opens for reading and writing - any type of modification can
 *      occur. If the file does not exist, this flag is effectively like
 *      'w'.
 *
 * Returns a newly allocated File object that can read and write data to the
 * file using a specific backend.
 *
 * @note: This method can be static.
 */
static boost::shared_ptr<bob::io::File>
make_file (const std::string& path, char mode) {
  return boost::make_shared<ImageNetpbmFile>(path, mode);
}

/**
 * Takes care of codec registration per se.
 */
static bool register_codec() {
  boost::shared_ptr<bob::io::CodecRegistry> instance =
    bob::io::CodecRegistry::instance();

  pm_init("bob",0);
  instance->registerExtension(".pbm", "PBM, indexed (libnetpbm)", &make_file);
  instance->registerExtension(".pgm", "PGM, indexed (libnetpbm)", &make_file);
  instance->registerExtension(".ppm", "PPM, indexed (libnetpbm)", &make_file);

  return true;

}

static bool codec_registered = register_codec();

