#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <ctype.h>
#include <alloca.h>

#define PORT 1337
#define MAX_SAFE_SIZE 256

struct req_data {
    size_t length;
    char *dest;
};

struct req_data global_req;

pthread_mutex_t dest_mutex = PTHREAD_MUTEX_INITIALIZER;

void trim_newline(char *str) {
    size_t len = strlen(str);
    if(len > 0 && (str[len-1]=='\n' || str[len-1]=='\r'))
        str[len-1] = '\0';
}

void *handle_update(void *arg) {
    int client_fd = *(int *)arg;
    free(arg);

    write(client_fd, "Set the size:\n", 15);
    char size_line[32] = {0};
    int n = read(client_fd, size_line, sizeof(size_line) - 1);
    if(n <= 0) {
        close(client_fd);
        return NULL;
    }
    trim_newline(size_line);

    size_t safe_length = 0;
    if (sscanf(size_line, "%zu", &safe_length) != 1) {
        write(client_fd, "Invalid SIZE format.\n", 22);
        close(client_fd);
        return NULL;
    }
    printf("[NeonPulse][UPDATE] Safe length set to %zu.\n", safe_length);

    char *local_buffer = alloca(safe_length);

    global_req.length = safe_length;

    write(client_fd, "Press ENTER to confirm update...\n", 34);
    char confirm[8] = {0};
    n = read(client_fd, confirm, sizeof(confirm)-1);

    pthread_mutex_lock(&dest_mutex);
    size_t i = 0;
    while(i < global_req.length) { 
        if(read(client_fd, local_buffer + i, 1) <= 0)
            break;
        i++;
    }

    global_req.dest = local_buffer;
    pthread_mutex_unlock(&dest_mutex);

    printf("[NeonPulse][UPDATE] Update complete. New message: %.20s...\n", global_req.dest);
    write(client_fd, "Update complete.\n", 18);
    return NULL;
}

void *handle_modify(void *arg) {
    int client_fd = *(int *)arg;
    free(arg);

    write(client_fd, "Set the new size:\n", 19);
    char size_line[32];
    memset(size_line, 0, sizeof(size_line));

    int n = read(client_fd, size_line, sizeof(size_line)-1);
    if(n <= 0) {
        close(client_fd);
        return NULL;
    }
    trim_newline(size_line);

    size_t new_length = 0;
    if (sscanf(size_line, "%zu", &new_length) != 1) {
        write(client_fd, "Invalid MODIFY format.\n", 24);
        close(client_fd);
        return NULL;
    }

    printf("[DataShadow][MODIFY] Before modification, length = %zu.\n", global_req.length);
    printf("[DataShadow][MODIFY] Changing length from %zu to %zu.\n", global_req.length, new_length);
    global_req.length = new_length;

    write(client_fd, "Modify complete.\n", 18);
    close(client_fd);
    return NULL;
}


void *handle_show(void *arg) {
    int client_fd = *(int *)arg;
    free(arg);
    
    char response[512];
    pthread_mutex_lock(&dest_mutex);
    snprintf(response, sizeof(response), "Current display message: %s\n", global_req.dest);
    pthread_mutex_unlock(&dest_mutex);
    
    write(client_fd, response, strlen(response));
    close(client_fd);
    return NULL;
}

int main() {
    
    int server_fd;
    struct sockaddr_in address;
    int addrlen = sizeof(address);

    global_req.dest = malloc(MAX_SAFE_SIZE);
    if (!global_req.dest) {
        exit(EXIT_FAILURE);
    }
    memset(global_req.dest, 0, MAX_SAFE_SIZE);
    strcpy(global_req.dest, "CYBERCORE PROPAGANDA");
    global_req.length = 128;

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        exit(EXIT_FAILURE);
    }
    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        exit(EXIT_FAILURE);
    }
    if (listen(server_fd, 5) < 0) {
        exit(EXIT_FAILURE);
    }
    printf("NeonPulse Server running on port %d...\n", PORT);
    
    while (1) {
        int *client_fd = malloc(sizeof(int));
        *client_fd = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen);
        if (*client_fd < 0) {
            perror("Accept error");
            free(client_fd);
            continue;
        }
        char cmd[16];
        memset(cmd, 0, sizeof(cmd));
        int n = read(*client_fd, cmd, sizeof(cmd)-1);
        if(n <= 0) {
            close(*client_fd);
            free(client_fd);
            continue;
        }
        cmd[strcspn(cmd, "\r\n")] = 0;
        printf("Command received: %s\n", cmd);
        
        pthread_t tid;
        if (strncmp(cmd, "UPDATE", 6) == 0) {
            pthread_create(&tid, NULL, handle_update, client_fd);
        } else if (strncmp(cmd, "MODIFY", 6) == 0) {
            pthread_create(&tid, NULL, handle_modify, client_fd);
        } else if (strncmp(cmd, "SHOW", 4) == 0) {
            pthread_create(&tid, NULL, handle_show, client_fd);
        } else {
            write(*client_fd, "Unknown command.\n", 18);
            close(*client_fd);
            free(client_fd);
            continue;
        }
        pthread_detach(tid);
    }
    
    free(global_req.dest);
    close(server_fd);
    return 0;
}
