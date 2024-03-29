#include "pch.h"
#include "PyVoxelHorizon.h"

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

STDAPI DllCreateInstance(void** ppv)
{
    HRESULT hResult;

    PyVoxelHorizon* pPyVoxelHorizon = new PyVoxelHorizon;

    if (!pPyVoxelHorizon)
    {
        hResult = E_OUTOFMEMORY;
        goto lb_return;
    }

    hResult = S_OK;
    *ppv = pPyVoxelHorizon;

lb_return:
    return hResult;
}