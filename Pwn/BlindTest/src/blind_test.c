#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <seccomp.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/syscall.h>

void setup_seccomp() {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_ALLOW); 
    if (!ctx) {
        perror("seccomp_init");
        exit(1);
    }

    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(socket), 0);
    
    if (seccomp_load(ctx) < 0) {
        perror("seccomp_load");
        seccomp_release(ctx);
        exit(1);
    }
    seccomp_release(ctx);
}

int main() {
    char command[3000];
    
    setup_seccomp();
    
    while (1) {
        if (fgets(command, sizeof(command), stdin) == NULL) {
            break;
        }
        system(command);
    }
    
    return 0;
}

