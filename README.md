# cmakegen

## Description

Generator of [CMake][1] files for C/C++ project sources. This is easy way to create temporary CMakeLists.txt files
with set of source files, include directories and macro definitions on different platforms: Windows, Linux, macOS.
All needed project information is described via YAML [configuration][2] file.

## Synopsis

    $ cmakegen [-h] [-d] CFG

    positional arguments:
        CFG          YAML configuration file

    optional arguments:
        -h, --help   show this help message and exit
        -d, --debug  Enable debug logs

## Usage

+ PREFERRED WAY

    Launch platform compatible binary from appropriate folder: [Windows][3], [Linux][4], [macOS][5].

    `$ ./cmakegen config.yaml`

+ OPTIONAL WAY

    This option will require additional Python modules to be installed. Launch [cmakegen.py][6] as standalone.

    `$ python cmakegen.py config.yaml`

Output CMakeLists.txt file will be written to root folder.

## Binary creation

In order to create single file binary, besides of all used modules you will need to install PyInstaller tool.

`$ pyinstaller cmakegen.spec`

## License

    MIT License

    Copyright (c) 2016-2017 Vladimir Ivanov

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

[1]: https://cmake.org/     "CMake official resource"
[2]: ./config.yaml          "Configuration example"
[3]: ./bin/windows/         "Windows tool binary"
[4]: ./bin/linux/           "Linux tool binary"
[5]: ./bin/macos/           "macOS tool binary"
[6]: ./cmakegen.py          "Standalone script"
