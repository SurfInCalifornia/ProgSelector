## About ProgSelector

ProgSelector is a fully offline tool for Microsoft Windows that allows you to choose whether you want to open a `.dll` file in Microsoft Visual Studio or dnSpy, provided that you have Visual Studio installed, along with dnSpy installed at C:\dnSpy. ProgSelector does not work for preview or insider versions of Visual Studio. ProgSelector works with the Community, Professional, and Enterprise versions of Visual Studio. For your information the attached MSI installer was made with Advanced Installer. The `.aip` files used to build the installer are not publicly available for privacy reasons. However, you are free to use, modify, and redistribute the installers under the license terms of this software. If you would like to set ProgSelector as your default application to open .dll files, you will need to set that manually as the MSI installer will not do that. ProgSelector does not auto-update. Different versions of ProgSelector are designed for different major releases of Visual Studio as follows:


1. ProgSelector 1 is designed for Visual Studio 2022

## Notes

- Do not attempt to use a version of ProgSelector with an incompatible major release of Visual Studio as it will cause ProgSelector to not function as intended
- Major releases of Visual Studio before the 2022 release do not have a corresponding version of ProgSelector
- Only the latest major release of ProgSelector will recieve updates of any kind
- ProgSelector 2.0.0 will be released in the near future to add support for Microsoft Visual Studio 2026
- On the date of the release of ProgSelector 2.0.0, shortly after it is published to this repository, the ProgSelector 1.0.0 MSI installer will be removed from the repository