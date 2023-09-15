#define PY_SSIZE_T_CLEAN

#include <windows.h>
#include <shlwapi.h>
#include <Python.h>

#pragma comment(lib, "shlwapi")

#define MODULE_NAME                             "Client_x64_release.exe"     // Name of process and module

// for 20230906 Build 33
#define GLOBAL_OFFSET_CGAME                     (0x0142158)                  // CGame

#define CODE_SIZE_CALL_SCENE_RUN_TRUE           13                           // Size of patch code for `OFFSET_CODE_CALL_SCENE_RUN_TRUE`
#define CODE_OFFSET_CALL_SCENE_RUN_TRUE         (0x005CE14)                  // `MOV this,qword ptr [RDI + 0x628]` ~ `CALL qword ptr [RAX + 0x50]` in CGame::Run with `g_gameOption.bShowEngineInfo == 0`

#define CODE_SIZE_CALL_SCENE_RUN_FALSE          13                           // Size of patch code for `OFFSET_CODE_CALL_SCENE_RUN_FALSE`
#define CODE_OFFSET_CALL_SCENE_RUN_FALSE        (0x005CDF9)                  // `MOV this,qword ptr [RDI + 0x628]` ~ `CALL qword ptr [RAX + 0x50]` in CGame::Run with `g_gameOption.bShowEngineInfo != 0`

#define MEMBER_OFFSET_SCENE                     (0x0000628)                  // Offset of member m_pScene in CGame
#define FUNCTION_OFFSET_SCENE_RUN               (0x0000050)                  // Function offset

bool        working                             = true;
bool        initialized                         = false;

LPBYTE      clientBaseAddress                   = NULL;

PyObject*   pythonVoxelHorizon                  = NULL;

PyObject*   pythonVoxelHorizonOnInitialize      = NULL;
void ExecutePythonOnInitialize(void* clientBasePointer, void* gameObjectPointer);

PyObject*   pythonVoxelHorizonOnLoop            = NULL;
void ExecutePythonOnLoop();

PyObject*   pythonVoxelHorizonOnStop            = NULL;
void ExecutePythonOnStop();

typedef unsigned long long PyAddress;
typedef void FuncSceneRun(DWORD64 thisPtr);

void Exit(int code)
{
    if (working)
    {
        working = false;

        if (Py_IsInitialized())
        {
            ExecutePythonOnStop();

            if (pythonVoxelHorizonOnInitialize != NULL)
            {
                Py_DECREF(pythonVoxelHorizonOnInitialize);
            }

            if (pythonVoxelHorizonOnLoop != NULL)
            {
                Py_DECREF(pythonVoxelHorizonOnLoop);
            }

            if (pythonVoxelHorizonOnStop != NULL)
            {
                Py_DECREF(pythonVoxelHorizonOnStop);
            }

            if (pythonVoxelHorizon != NULL)
            {
                Py_DECREF(pythonVoxelHorizon);
            }

            Py_Finalize();
        }
    }

    exit(code);
}

void CrashReport(int errorCode, const wchar_t* message, ...)
{

    va_list argumentPointer;
    va_start(argumentPointer, message);
    size_t length = _vscwprintf(message, argumentPointer);
    wchar_t* buffer = new wchar_t[length + 1];

    vswprintf_s(buffer, length + 1, message, argumentPointer);
    va_end(argumentPointer);

    MessageBoxW(NULL, buffer, L"PyVoxelHorizon Crash", MB_OK);

    delete[] buffer;

    Exit(errorCode);
}

void CrashReportForPythonException()
{
    if (PyErr_Occurred())
    {
        PyObject* type;
        PyObject* value;
        PyObject* traceback;

        PyErr_Fetch(&type, &value, &traceback);

        if (type == NULL)
        {
            return;
        }

        PyErr_NormalizeException(&type, &value, &traceback);

        if (traceback == NULL)
        {
            CrashReport(EXIT_FAILURE, L"Failure get traceback");
        }

        PyException_SetTraceback(value, traceback);

        PyObject* pythonTracebackModule = PyImport_ImportModule("traceback");

        if (pythonTracebackModule == NULL)
        {
            CrashReport(EXIT_FAILURE, L"Failure format python exception");
        }

        PyObject* pythonFormatException = PyObject_GetAttrString(pythonTracebackModule, "format_exception");

        if (pythonFormatException == NULL)
        {
            CrashReport(EXIT_FAILURE, L"Failure format python exception");
        }

        PyObject* pythonFormatResult = PyObject_CallObject(pythonFormatException, PyTuple_Pack(3, type, value, traceback));

        if (pythonFormatResult == NULL)
        {
            CrashReport(EXIT_FAILURE, L"Failure format python exception");
        }

        PyObject* pythonJoinResult = PyUnicode_Join(PyUnicode_FromString("\n"), pythonFormatResult);

        if (pythonJoinResult == NULL)
        {
            CrashReport(EXIT_FAILURE, L"Failure format python exception");
        }

        const char* message = PyUnicode_AsUTF8(pythonJoinResult);

        CrashReport(EXIT_FAILURE, L"Crash in Python\r\n%S", message);
    }
}

void OnGameLoop()
{
    LPBYTE gameObjectPointer = (LPBYTE)(*(DWORD64*)(clientBaseAddress + GLOBAL_OFFSET_CGAME));
    LPBYTE sceneObjectPointer = (LPBYTE)(*(DWORD64*)(gameObjectPointer + MEMBER_OFFSET_SCENE));
    LPBYTE sceneObjectFunctionTablePointer = (LPBYTE)(*(DWORD64*)sceneObjectPointer);
    LPBYTE sceneRunFunctionPointer = (LPBYTE)(*(DWORD64*)(sceneObjectFunctionTablePointer + FUNCTION_OFFSET_SCENE_RUN));

    if (working)
    {
        if (!initialized)
        {
            initialized = true;
        
            ExecutePythonOnInitialize(clientBaseAddress, gameObjectPointer);
        }

        ExecutePythonOnLoop();
    }

    // Call CGame->m_pScene->Run();
    ((FuncSceneRun*)sceneRunFunctionPointer)((DWORD64)sceneObjectPointer);
}

void ExecutePythonOnInitialize(void* clientBasePointer, void* gameObjectPointer)
{
    if (pythonVoxelHorizon == NULL || pythonVoxelHorizonOnInitialize == NULL)
    {
        return;
    }

    PyObject* pythonModuleAddress = PyLong_FromUnsignedLongLong((PyAddress)clientBasePointer);
    PyObject* pythonGameObjectAddress = PyLong_FromUnsignedLongLong((PyAddress)gameObjectPointer);
    PyObject* pythonArgument = PyTuple_Pack(2, pythonModuleAddress, pythonGameObjectAddress);
    PyObject* pythonReturnValue = PyObject_CallObject(pythonVoxelHorizonOnInitialize, pythonArgument);

    if (pythonReturnValue == NULL)
    {
        CrashReportForPythonException();
    }

    Py_DECREF(pythonReturnValue);
    Py_DECREF(pythonArgument);
    Py_DECREF(pythonGameObjectAddress);
    Py_DECREF(pythonModuleAddress);
}

void ExecutePythonOnLoop()
{
    if (pythonVoxelHorizon == NULL || pythonVoxelHorizonOnLoop == NULL)
    {
        return;
    }

    PyObject* pythonArgument = PyTuple_Pack(0);
    PyObject* pythonReturnValue = PyObject_CallObject(pythonVoxelHorizonOnLoop, pythonArgument);

    if (pythonReturnValue == NULL)
    {
        CrashReportForPythonException();
    }

    Py_DECREF(pythonReturnValue);
    Py_DECREF(pythonArgument);
}

void ExecutePythonOnStop()
{
    if (pythonVoxelHorizon == NULL || pythonVoxelHorizonOnStop == NULL)
    {
        return;
    }

    PyObject* pythonArgument = PyTuple_Pack(0);
    PyObject* pythonReturnValue = PyObject_CallObject(pythonVoxelHorizonOnStop, pythonArgument);

    if (pythonReturnValue == NULL)
    {
        CrashReportForPythonException();
    }

    Py_DECREF(pythonReturnValue);
    Py_DECREF(pythonArgument);
}

bool PatchCode(LPBYTE targetAddress, DWORD64 codeSize) {
    DWORD oldMemoryProtect;

    if (targetAddress == NULL)
    {
        return false;
    }

    // Modify memory protection
    VirtualProtect((LPVOID)targetAddress, codeSize, PAGE_EXECUTE_READWRITE, &oldMemoryProtect);

    BYTE codes[] = {
        0x48, 0xB8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,     // MOV RAX, FUNCTION ADDRESS (LONG OP)
        0xFF, 0xD0                                                      // CALL RAX
    };

    *((DWORD64*)(codes + 2)) = (DWORD64)((LPBYTE)&OnGameLoop);

    // Patch to hook code
    for (int index = 0; index < sizeof(codes); index++)
    {
        *((LPBYTE)targetAddress + index) = codes[index];
    }

    // Fill NOP
    for (int index = sizeof(codes); index < codeSize; index++)
    {
        *((LPBYTE)targetAddress + index) = 0x90;
    }

    // Restore memory protection
    VirtualProtect(targetAddress, codeSize, oldMemoryProtect, &oldMemoryProtect);
}

bool HookGameLoop()
{
    HMODULE moduleHandle;

    moduleHandle = GetModuleHandle(TEXT(MODULE_NAME));

    if (moduleHandle == NULL)
    {
        return false;
    }

    clientBaseAddress = (LPBYTE) moduleHandle;

    PatchCode(clientBaseAddress + CODE_OFFSET_CALL_SCENE_RUN_TRUE, CODE_SIZE_CALL_SCENE_RUN_TRUE);
    PatchCode(clientBaseAddress + CODE_OFFSET_CALL_SCENE_RUN_FALSE, CODE_SIZE_CALL_SCENE_RUN_FALSE);
}

bool GetSimpleFileName(wchar_t* destination, wchar_t* path)
{
    wchar_t* fileNameOffset = PathFindFileNameW(path);

    if (fileNameOffset == path)
    {
        return false;
    }

    int position = 0;

    do
    {
        if (fileNameOffset[position] == '.')
        {
            destination[position] = '\0';
            break;
        }

        destination[position] = fileNameOffset[position];

    } while (fileNameOffset[position++] != '\0');

    return true;
}

extern "C"
__declspec(dllexport) void InitializeBridge(void* arguments)
{
    int pathLength = wcsnlen_s((wchar_t*)arguments, MAX_PATH);
    wchar_t wideScriptFilePath[MAX_PATH];
    wchar_t wideScriptFileDirectoryPath[MAX_PATH];
    wchar_t wideScriptFileName[MAX_PATH];
    char scriptFileName[MAX_PATH];

    if (pathLength + 1 > MAX_PATH)
    {
        CrashReport(EXIT_FAILURE, L"Wrong argument for `InitializeBridge`");
    }

    wcscpy_s(wideScriptFilePath, pathLength + 1, (wchar_t*)arguments);
    wcscpy_s(wideScriptFileDirectoryPath, pathLength + 1, (wchar_t*)arguments);
    wcscpy_s(wideScriptFileName, pathLength + 1, (wchar_t*)arguments);

    if (!PathRemoveFileSpecW(wideScriptFileDirectoryPath))
    {
        CrashReport(EXIT_FAILURE, L"Failure `PathRemoveFileSpecW`");
    }
    
    if (!GetSimpleFileName(wideScriptFileName, wideScriptFilePath))
    {
        CrashReport(EXIT_FAILURE, L"Failure `GetSimpleFileName`");
    }

    size_t convertedSize;

    if (wcstombs_s(&convertedSize, scriptFileName, wideScriptFileName, MAX_PATH) < 0)
    {
        CrashReport(EXIT_FAILURE, L"Failure convert wide character script file name to normal character.");
    }

    scriptFileName[convertedSize] = '\0';

    Py_Initialize();
    
    PyObject* pythonSysModule = PyImport_ImportModule("sys");

    if (pythonSysModule == NULL)
    {
        CrashReportForPythonException();
    }

    PyObject* pythonSysPath = PyObject_GetAttrString(pythonSysModule, "path");

    if (pythonSysPath == NULL)
    {
        CrashReportForPythonException();
    }
    PyObject* pythonScriptFileDirectoryPath = PyUnicode_FromWideChar(wideScriptFileDirectoryPath, wcsnlen_s(wideScriptFileDirectoryPath, MAX_PATH));

    if (pythonScriptFileDirectoryPath == NULL)
    {
        CrashReportForPythonException();
    }

    PyList_Append(pythonSysPath, pythonScriptFileDirectoryPath);
    
    PyObject* pythonVoxelHorizonModule = PyImport_ImportModule(scriptFileName);

    if (pythonVoxelHorizonModule == NULL)
    {
        CrashReportForPythonException();
    }

    PyObject* pythonVoxelHorizonClass = PyObject_GetAttrString(pythonVoxelHorizonModule, "PyVoxelHorizon");

    if (pythonVoxelHorizonClass == NULL)
    {
        CrashReportForPythonException();
    }

    PyObject* pythonArgument = PyTuple_Pack(1, pythonScriptFileDirectoryPath);

    if (pythonArgument == NULL)
    {
        CrashReportForPythonException();
    }

    pythonVoxelHorizon = PyObject_CallObject(pythonVoxelHorizonClass, pythonArgument);

    if (pythonVoxelHorizon == NULL)
    {
        CrashReportForPythonException();
    }
    
    // Function Getter
    pythonVoxelHorizonOnInitialize = PyObject_GetAttrString(pythonVoxelHorizon, "on_initialize");

    if (pythonVoxelHorizonOnInitialize == NULL)
    {
        CrashReportForPythonException();
    }

    pythonVoxelHorizonOnLoop = PyObject_GetAttrString(pythonVoxelHorizon, "on_loop");

    if (pythonVoxelHorizonOnLoop == NULL)
    {
        CrashReportForPythonException();
    }
    
    pythonVoxelHorizonOnStop = PyObject_GetAttrString(pythonVoxelHorizon, "on_stop");

    if (pythonVoxelHorizonOnStop == NULL)
    {
        CrashReportForPythonException();
    }

    Py_DECREF(pythonArgument);
    Py_DECREF(pythonVoxelHorizonClass);
    Py_DECREF(pythonVoxelHorizonModule);
    Py_DECREF(pythonScriptFileDirectoryPath);
    Py_DECREF(pythonSysPath);
    Py_DECREF(pythonSysModule);
    
    if (!HookGameLoop())
    {
        CrashReport(EXIT_FAILURE, L"Failure hook game loop");
    }
}

BOOL APIENTRY DllMain(HMODULE module, DWORD  reason, LPVOID reserved)
{
    switch (reason)
    {
    case DLL_PROCESS_ATTACH:
        break;
    case DLL_THREAD_ATTACH:
        break;
    case DLL_THREAD_DETACH:
        break;
    case DLL_PROCESS_DETACH:
        Exit(EXIT_SUCCESS);

        break;
    }

    return TRUE;
}

