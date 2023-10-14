#ifndef PCH_H
#define PCH_H

#ifdef _DEBUG
#define _CRTDBG_MAP_ALLOC
#include <crtdbg.h>
#define new new(_NORMAL_BLOCK, __FILE__, __LINE__)
#endif

typedef unsigned long long PyAddress;

// Windows Header
#include <initguid.h>
#include <ole2.h>
#include <stdlib.h>
#include <windows.h>
#include <shlwapi.h>

#pragma comment(lib, "shlwapi")

// Voxel Horizon Header
#include <IGameHookController.h>

// Python Header
#include <Python.h>

#endif