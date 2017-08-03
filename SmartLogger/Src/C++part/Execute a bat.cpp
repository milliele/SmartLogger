#include <stdio.h>
#include <windows.h>
#include <tchar.h>
#include <string>

int main(int argc, char** argv)
{
    SHELLEXECUTEINFO sei={sizeof(SHELLEXECUTEINFO)};
    sei.lpVerb=TEXT("runas");
    if(argc>1)
    {
        sei.lpFile=TEXT(argv[1]);//add  application  which you want to run as administrator here
        sei.lpParameters=TEXT("");
        sei.nShow=SW_SHOWNORMAL;//without this,the windows will be hiden
        if(!ShellExecuteEx(&sei)){
            DWORD dwStatus=GetLastError();
            if(dwStatus==ERROR_CANCELLED){
                printf("³É¹¦");
            }
            else
            if(dwStatus==ERROR_FILE_NOT_FOUND){
                printf("Ê§°Ü");
            }
        }
    }
}
