%% Bowen INDOT Bridge Research - Hardness Samples t-tests
clc; close; close all;  % -------------------------------------------------------
% This script reads hardness data from an Excel file, then for each "flange" and "web" runs a Levene
% test for equal variances and an independent t‑test against the ambient flange and web values.

%% Read the spreadsheet (sheet 1)
outputFile = 'INDOT_Hardness_test_cleaned_file.xlsx';
Table_Flange = readtable('INDOT_Hardness_test_cleaned_file.xlsx', 'Sheet', "First HRB Ignored Flange"); % this line read Flange in the file
Table_Web = readtable('INDOT_Hardness_test_cleaned_file.xlsx', 'Sheet', "First HRB Ignored Web"); % this line read Web 1 in the file

titles_Flange = Table_Flange.Name; 
R1_Flange = Table_Flange.Reading1;  
R2_Flange = Table_Flange.Reading2;  
R3_Flange = Table_Flange.Reading3; R4_Flange = Table_Flange.Reading4; R5_Flange = Table_Flange.Reading5;  
R6_Flange = Table_Flange.Reading6; R7_Flange = Table_Flange.Reading7;  R8_Flange = Table_Flange.Reading8; 
R9_Flange = Table_Flange.Reading9; R10_Flange = Table_Flange.Reading10; % this line import all Flange columns

titles_Web = Table_Web.Name; R1_Web = Table_Web.Reading1;  R2_Web = Table_Web.Reading2;  
R3_Web = Table_Web.Reading3; R4_Web = Table_Web.Reading4; R5_Web = Table_Web.Reading5;  
R6_Web = Table_Web.Reading6; R7_Web = Table_Web.Reading7;  R8_Web = Table_Web.Reading8; 
R9_Web = Table_Web.Reading9; R10_Web = Table_Web.Reading10; % this line import all Flange columns

%% Define ambient flange and web (first row values of R1–R4)
amb_flange = [ R1_Flange(1), R2_Flange(1), R3_Flange(1), R4_Flange(1), R5_Flange(1)];
amb_web = [R1_Web(2), R2_Web(2), R3_Web(2), R4_Web(2), R5_Web(2)];

%% Loop over all flanges from index 3 onward (to mirror Python's 2:)
for i = 3 : length(titles_Flange)
    if i == 3
        fprintf("\n  Water Cooled Flange Samples \n \n")
    end
    % collect this flange’s readings (R1–R10 at row i)
    data = [R1_Flange(i), R2_Flange(i), R3_Flange(i), R4_Flange(i), R5_Flange(i), R6_Flange(i), R7_Flange(i), R8_Flange(i), R9_Flange(i), R10_Flange(i)];

    % Levene s test for equal variances
    group = [ones(size(amb_flange)), 2*ones(size(data))]'; %Combine the two groups and make a grouping vector
    values = [ amb_flange, data ]'; %This combines the amb_fl vector and data vector
    equalVar = (vartestn(values, group, 'TestType', 'LeveneAbsolute', 'Display', 'off') > 0.05); % returns 1 if equal variance and 0 if not
    
    if i == 13
        fprintf("\n  Air Cooled Flange Samples \n \n")
    end 
    % performs Two‑sample t‑test 
    vartype = 'unequal';
    if equalVar == 1
        vartype = 'equal';
    end
    [~, p_ttest_flange(i-2)] = ttest2(amb_flange, data, 'Vartype', vartype);
    
    if p_ttest_flange(i-2) <= 0.05
        fprintf("The p-value for %s FLange is %.10f => Different\n", string(titles_Flange(i)), p_ttest_flange(i-2));
    else
        fprintf("The p-value for %s Flange is %.10f => Not Different\n", string(titles_Flange(i)), p_ttest_flange(i-2));
    end
end

%% Loop over all Web from index 3 onward (to mirror Python's 2:) and perform 2 sample t-test
for i = 3 : length(titles_Web)
    if i == 3
        fprintf("\n  Water Cooled Web Samples \n \n")
    end
    % collect this flange’s readings (R1–R10 at row i)
    data = [R2_Web(i), R3_Web(i), R4_Web(i), R5_Web(i), R6_Web(i), R7_Web(i), R8_Web(i), R9_Web(i), R10_Web(i)];

    % Levene s test for equal variances
    group = [ones(size(amb_web)), 2*ones(size(data))]'; %Combine the two groups and make a grouping vector
    values = [ amb_web, data ]'; %This combines the amb_fl vector and data vector
    equalVar = (vartestn(values, group, 'TestType', 'LeveneAbsolute', 'Display', 'off') > 0.05); % returns 1 if euqal var and 0 if not
    if i == 23
        fprintf("\n  Air Cooled Web Samples \n \n")
    end 
    % performs Two‑sample t‑test 
    vartype = 'unequal';
    if equalVar == 1
        vartype = 'equal';
    end
    [~, p_ttest_web(i-2)] = ttest2(amb_web, data, 'Vartype', vartype);

    if p_ttest_web(i-2) <= 0.05
        fprintf("The p-value for %s Web is %.10f => Different\n", string(titles_Web(i)), p_ttest_web(i-2));
    else
        fprintf("The p-value for %s Web is %.10f => Not Different\n", string(titles_Web(i)), p_ttest_web(i-2));
    end
end

%% import the data back into the excel sheet
% Define column where you want to insert p-values (e.g., column U = 21)
col = 17;

% Write headers manually
%writecell({'pvalue'}, outputFile, 'Sheet', "First HRB Ignored Flange", 'Range', [char(64+col) '5']); % put pvalue row 5
%writecell({'pvalue'}, outputFile, 'Sheet', "First HRB Ignored Web",    'Range', [char(64+col) '5']);

% Write p_ttest_flange (starting from row 3)
writematrix(p_ttest_flange', outputFile, 'Sheet', "First HRB Ignored Flange", 'Range', [char(64+col) '8']); %start writting at row 8

% Write p_ttest_web (starting from row 3)
writematrix(p_ttest_web', outputFile, 'Sheet', "First HRB Ignored Web", 'Range', [char(64+col) '8']); %start writting at row 8

