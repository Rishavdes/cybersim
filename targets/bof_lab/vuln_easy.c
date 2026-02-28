/*
 * CyberSim BOF Lab - Vulnerable Binary (Easy Mode)
 * 
 * Vulnerability: Stack-based buffer overflow via gets()
 * The win() function prints the flag. Player must overwrite the return
 * address to call win() instead of returning normally.
 *
 * Compile: gcc -o vuln_easy vuln_easy.c -fno-stack-protector -z execstack -no-pie
 * No protections: No ASLR, No DEP, No Canary, No PIE
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void win() {
    char *flag = getenv("CYBERSIM_FLAG");
    if (flag) {
        printf("\n[!] BUFFER OVERFLOW SUCCESSFUL!\n");
        printf("[FLAG] %s\n\n", flag);
    } else {
        printf("\n[!] Flag not set. Run with CYBERSIM_FLAG env.\n");
    }
    fflush(stdout);
    exit(0);
}

void vulnerable() {
    char buffer[64];
    printf("Enter your name: ");
    fflush(stdout);
    gets(buffer);  /* VULNERABLE: No bounds checking! */
    printf("Hello, %s!\n", buffer);
    fflush(stdout);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    printf("╔══════════════════════════════════════╗\n");
    printf("║   CyberSim BOF Lab - Easy Mode       ║\n");
    printf("║   Binary: vuln_easy (No Protections)  ║\n");
    printf("╚══════════════════════════════════════╝\n\n");
    printf("Hint: The win() function is at %p\n", (void *)win);
    printf("Hint: The buffer is 64 bytes. What happens if you send more?\n\n");
    fflush(stdout);

    vulnerable();

    printf("Program exited normally. Try harder!\n");
    return 0;
}
