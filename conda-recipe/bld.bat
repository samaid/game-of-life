if "%PYTHON%"=="" (set PYTHON=python)
"%PYTHON%" setup.py clean --all
if errorlevel 1 exit 1

"%PYTHON%" setup.py install
if errorlevel 1 exit 1

if NOT "%WHEELS_OUTPUT_FOLDER%"=="" (
    rem Install and assemble wheel package from the build bits
    "%PYTHON%" setup.py install bdist_wheel %SKBUILD_ARGS%
    if errorlevel 1 exit 1
    copy dist\dpctl*.whl %WHEELS_OUTPUT_FOLDER%
    if errorlevel 1 exit 1
) else (
    rem Only install
    "%PYTHON%" -m pip install .
    if errorlevel 1 exit 1
)
