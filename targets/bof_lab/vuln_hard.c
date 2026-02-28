/*
 * CyberSim BOF Lab - Vulnerable Binary (Hard Mode)
 *
 * Vulnerability: Format string + stack buffer overflow
 * Full protections: ASLR ON, DEP ON, Partial RELRO
 * Player must leak a libc address via format string, then exploit BOF
 *
 * Compile: gcc -o vuln_hard vuln_hard.c -fno-stack-protector -pie -fPIC
 * Protections: ASLR ON, DEP ON, PIE ON, No Canary
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void setup_flag() {
    char *flag = getenv("CYBERSIM_FLAG");
    if (flag) {
        FILE *f = fopen("/root/flag.txt", "w");
        if (f) {
            fprintf(f, "%s\n", flag);
            fclose(f);
        }
    }
}

void leak_phase() {
    char input[128];
    printf("DEBUG Console > ");
    fflush(stdout);
    fgets(input, sizeof(input), stdin);
    printf("Echo: ");
    printf(input);  /* FORMAT STRING VULNERABILITY - can leak stack/libc addresses */
    fflush(stdout);
}

void exploit_phase() {
    char buffer[64];
    printf("Enter admin password: ");
    fflush(stdout);
    read(STDIN_FILENO, buffer, 256);  /* BOF - same as normal but with ASLR */
    printf("Verifying...\n");
    fflush(stdout);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    setup_flag();

    printf("╔══════════════════════════════════════╗\n");
    printf("║  CyberSim BOF Lab - Hard Mode          ║\n");
    printf("║  Binary: vuln_hard (Full Protection)    ║\n");
    printf("╚══════════════════════════════════════╝\n\n");
    printf("Hint: Two-stage exploit needed.\n");
    printf("Hint: Stage 1 = Leak libc address. Stage 2 = ROP.\n");
    printf("Hint: The flag is in /root/flag.txt\n\n");
    fflush(stdout);

    /* Stage 1: Format string to leak addresses */
    printf("[Phase 1: Debug Console]\n");
    leak_phase();

    /* Stage 2: Buffer overflow with ASLR active */
    printf("\n[Phase 2: Authentication]\n");
    exploit_phase();

    printf("Authentication failed.\n");
    return 0;
}
