/*
 * CyberSim BOF Lab - Vulnerable Binary (Normal Mode)
 *
 * Vulnerability: Stack-based buffer overflow via read()
 * DEP is ON - no stack execution allowed.
 * Player must use ret2libc / ROP to call system("/bin/sh")
 * then read /root/flag.txt
 *
 * Compile: gcc -o vuln_normal vuln_normal.c -fno-stack-protector -no-pie
 * Protections: DEP ON, No Canary, No PIE, No ASLR
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void setup_flag() {
    /* Write flag to /root/flag.txt at startup */
    char *flag = getenv("CYBERSIM_FLAG");
    if (flag) {
        FILE *f = fopen("/root/flag.txt", "w");
        if (f) {
            fprintf(f, "%s\n", flag);
            fclose(f);
        }
    }
}

void vulnerable() {
    char buffer[64];
    printf("Enter the secret passphrase: ");
    fflush(stdout);
    read(STDIN_FILENO, buffer, 256);  /* VULNERABLE: reads 256 into 64-byte buffer */
    printf("Checking passphrase: %s\n", buffer);
    fflush(stdout);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    setup_flag();

    printf("╔══════════════════════════════════════╗\n");
    printf("║  CyberSim BOF Lab - Normal Mode       ║\n");
    printf("║  Binary: vuln_normal (DEP Enabled)     ║\n");
    printf("╚══════════════════════════════════════╝\n\n");
    printf("Hint: Stack is NOT executable. You need ROP/ret2libc.\n");
    printf("Hint: Try: ROPgadget --binary vuln_normal --ropchain\n");
    printf("Hint: The flag is in /root/flag.txt\n\n");
    fflush(stdout);

    vulnerable();

    printf("Access denied.\n");
    return 0;
}
