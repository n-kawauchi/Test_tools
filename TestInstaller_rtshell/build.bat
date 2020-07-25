@echo off

"%WIX%"bin\candle -arch x64 TestRTShell.wxs
"%WIX%"bin\light TestRTShell.wixobj -o TestRTShell_x64.msi

del *.wixobj *.wixpdb
