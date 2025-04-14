#import <Foundation/Foundation.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

@interface Patient : NSObject {
    id patientID; // Change: from NSString* to id
    NSInteger vitalStatus;
}
@property (nonatomic, assign) id patientID;  // Change here
@property (nonatomic, assign) NSInteger vitalStatus;
- (void)setPatientInfoWithId:(NSString *)pid status:(NSInteger)status;
- (void)displayPatientInfo;
@end

@implementation Patient
@synthesize patientID, vitalStatus;
- (void)setPatientInfoWithId:(NSString *)pid status:(NSInteger)status {
    self.patientID = pid;
    self.vitalStatus = status;
}
- (void)displayPatientInfo {
    NSLog(@"Patient ID: %@", self.patientID);
    NSLog(@"Vital Status: %ld", (long)self.vitalStatus);
}
@end

@interface NeuroReport : NSObject {
    char *reportData;
    Patient *associatedPatient;
}
@property (nonatomic, assign) char *reportData;
@property (nonatomic, retain) Patient *associatedPatient;
- (void)createReportWithSize:(size_t)size;
- (void)modifyReport;
@end

@implementation NeuroReport
@synthesize reportData, associatedPatient;
- (void)createReportWithSize:(size_t)size {
    reportData = malloc(size);
    if (reportData == NULL) {
        NSLog(@"Memory allocation error.");
        return;
    }
    
    NSLog(@"Enter report content:");
    if (fgets(reportData, size, stdin) == NULL) {
        NSLog(@"Error reading input.");
        return;
    }
    size_t len = strlen(reportData);
    if (len > 0 && reportData[len - 1] == '\n') {
        reportData[len - 1] = '\0';
    }
}

- (void)modifyReport {
    if (reportData != NULL) {
        free(reportData);
        reportData = NULL;
    }
    size_t size = 160; 
    reportData = malloc(size);
    if (reportData == NULL) {
        NSLog(@"Memory allocation error during modification.");
        return;
    }
    NSLog(@"Enter new report content:");
    if (fgets(reportData, size, stdin) == NULL) {
        NSLog(@"Error reading input.");
        return;
    }
    size_t len = strlen(reportData);
    if (len > 0 && reportData[len - 1] == '\n') {
        reportData[len - 1] = '\0';
    }
    NSLog(@"Report modified.");
}
@end

int main(int argc, const char * argv[]) {
    setvbuf(stdout, NULL, _IONBF, 0);
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
    
    NSMutableArray *patients = [NSMutableArray array];
    NSMutableArray *reports = [NSMutableArray array];
    
    int choice = 0;
    char bufferInput[128];
    int i;    
    while (1) {
        NSLog(@"\n========================================\n Trauma Team Emergency Interface - Neon City\n========================================\n1. Create a patient record\n2. Display all patient records\n3. Modify a patient's ID\n4. Generate a report for a patient\n5. Modify the report\n6. Check if the patient is cured\n7. Quit\nYour choice:");
        
        fgets(bufferInput, sizeof(bufferInput), stdin);
        choice = atoi(bufferInput);
        
        if (choice == 1) {
            Patient *p = [[Patient alloc] init];
            NSLog(@"Enter patient ID:");
            fgets(bufferInput, sizeof(bufferInput), stdin);
            bufferInput[strcspn(bufferInput, "\n")] = 0;
            NSString *pid = [NSString stringWithCString:bufferInput encoding:NSUTF8StringEncoding];
            NSLog(@"Enter vital status:");
            fgets(bufferInput, sizeof(bufferInput), stdin);
            int status = atoi(bufferInput);
            [p setPatientInfoWithId:pid status:status];
            [patients addObject:p];
            [p release];
            NSLog(@"Patient record created.");
        }
        else if (choice == 2) {
            NSLog(@"--- Patient Records ---");
            for (i = 0; i < [patients count]; i++) {
                NSLog(@"Index %d :", i);
                [[patients objectAtIndex:i] displayPatientInfo];
            }
        }
        else if (choice == 3) {
            NSLog(@"Enter patient index:");
            fgets(bufferInput, sizeof(bufferInput), stdin);
            int index = atoi(bufferInput);
            if (index >= 0 && index < [patients count]) {
                NSAutoreleasePool *tempPool = [[NSAutoreleasePool alloc] init];
                NSLog(@"Enter new patient ID:");
                fgets(bufferInput, sizeof(bufferInput), stdin);
                bufferInput[strcspn(bufferInput, "\n")] = 0;
                NSString *newID = [NSString stringWithFormat:@"%s", bufferInput];
                Patient *p = [patients objectAtIndex:index];
                
                if ([newID isEqual:p.patientID]) {
                    NSLog(@"Error: new patient ID is the same as the old one!");
                } else {
                    p.patientID = newID;
                    NSLog(@"ID modified!");
                }
                
                [tempPool drain];
            } else {
                NSLog(@"Invalid index.");
            }
        }
        else if (choice == 4) {
            if ([patients count] == 0) {
                NSLog(@"No patients available.");
            } else {
                NSLog(@"Enter patient index:");
                fgets(bufferInput, sizeof(bufferInput), stdin);
                int index = atoi(bufferInput);
                if (index >= 0 && index < [patients count]) {
                    NeuroReport *newReport = [[NeuroReport alloc] init];
                    newReport.associatedPatient = [[patients objectAtIndex:index] retain];
                    [newReport createReportWithSize:160];
                    [reports addObject:newReport];
                    [newReport.associatedPatient release];
                    [newReport release];
                    NSLog(@"Report generated.");
                } else {
                    NSLog(@"Invalid index.");
                }
            }
        }
        else if (choice == 5) {
            NSLog(@"Enter report index:");
            fgets(bufferInput, sizeof(bufferInput), stdin);
            int index = atoi(bufferInput);
            if (index >= 0 && index < [reports count]) {
                NeuroReport *r = [reports objectAtIndex:index];
                [r modifyReport];
            } else {
                NSLog(@"Invalid index.");
            }
        }
        else if (choice == 6) {
            NSLog(@"Enter patient index to check for cured status:");
            fgets(bufferInput, sizeof(bufferInput), stdin);
            int index = atoi(bufferInput);
            if (index >= 0 && index < [patients count]) {
                Patient *p = [patients objectAtIndex:index];
                Class patientIDClass = [p.patientID class];
                NSString *className = NSStringFromClass(patientIDClass);
                NSLog(@"%@", className);
                if ([className isEqualToString:@"Cured"]) {
                    NSLog(@"Patient is cured.");
                    system("/bin/sh");
                } else {
                    NSLog(@"Patient is not cured.");
                }
            } else {
                NSLog(@"Invalid index.");
            }
        }
        else if (choice == 7) {
            return 0;
        }
        else {
            NSLog(@"Invalid option.");
        }
        
    }
    
    [reports release];
    [patients release]; 
    [pool drain];
    return 0;
}
