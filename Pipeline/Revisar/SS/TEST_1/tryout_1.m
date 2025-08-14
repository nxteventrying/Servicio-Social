% Clear workspace and set format
clear
sqrt2 = sqrt(2);
format bank

% Load file and extract data
fileName = input('Indicate the file name with extension in quotes: ', 's');
data = load(fileName, '-ascii');
timeData = data(:,1);  % Time data
rrIntervals = data(:,2);  % RR intervals

% Remove zero RR values and store corresponding time values
validIndices = rrIntervals > 0;
cleanedRRIntervals = rrIntervals(validIndices);
cleanedTimeData = timeData(validIndices);

% Initialize counters for phase transitions
phaseIndices = struct('restStart', 0, 'warmUpStart', 0, 'exerciseStart', 0, ...
                      'recoveryStart', 0, 'phaseEnd1', 0, 'phaseEnd2', 0, ...
                      'phaseEnd3', 0, 'phaseEnd4', 0, 'phaseEnd5', 0, ...
                      'phaseEnd6', 0, 'phaseEnd7', 0);

% Detect phase transition points
for i = 1:length(cleanedRRIntervals)
    if cleanedTimeData(i) > 1 && phaseIndices.restStart == 0
        phaseIndices.restStart = i;
    end
    if cleanedTimeData(i) > 7 && phaseIndices.warmUpStart == 0
        phaseIndices.warmUpStart = i;
    end
    if cleanedTimeData(i) > 14 && phaseIndices.exerciseStart == 0
        phaseIndices.exerciseStart = i;
    end
    if cleanedTimeData(i) > 20 && phaseIndices.recoveryStart == 0
        phaseIndices.recoveryStart = i;
    end
    % Define end of phases based on specific time thresholds
    if cleanedTimeData(i) > 6 && phaseIndices.phaseEnd1 == 0
        phaseIndices.phaseEnd1 = i;
    end
    if cleanedTimeData(i) > 9 && phaseIndices.phaseEnd2 == 0
        phaseIndices.phaseEnd2 = i;
    end
    if cleanedTimeData(i) > 14 && phaseIndices.phaseEnd3 == 0
        phaseIndices.phaseEnd3 = i;
    end
    if cleanedTimeData(i) > 19 && phaseIndices.phaseEnd4 == 0
        phaseIndices.phaseEnd4 = i;
    end
    if cleanedTimeData(i) > 25 && phaseIndices.phaseEnd5 == 0
        phaseIndices.phaseEnd5 = i;
    end
    if cleanedTimeData(i) > 30 && phaseIndices.phaseEnd6 == 0
        phaseIndices.phaseEnd6 = i;
    end
    if cleanedTimeData(i) > 31 && phaseIndices.phaseEnd7 == 0
        phaseIndices.phaseEnd7 = i;
    end
end

% Assign cleaned RR intervals to a variable for further analysis
RR = cleanedRRIntervals;

% Compute mean and standard deviation for different phases
meanRest = mean(RR(phaseIndices.restStart:phaseIndices.phaseEnd1));
stdRest = std(RR(phaseIndices.restStart:phaseIndices.phaseEnd1));

meanWarmUp = mean(RR(phaseIndices.warmUpStart:phaseIndices.phaseEnd2));
stdWarmUp = std(RR(phaseIndices.warmUpStart:phaseIndices.phaseEnd2));

meanExercise = mean(RR(phaseIndices.exerciseStart:phaseIndices.phaseEnd4));
stdExercise = std(RR(phaseIndices.exerciseStart:phaseIndices.phaseEnd4));

meanRecovery = mean(RR(phaseIndices.recoveryStart:phaseIndices.phaseEnd6));
stdRecovery = std(RR(phaseIndices.recoveryStart:phaseIndices.phaseEnd6));

% Calculate SD1 and SD2 for each phase
calculateSD = @(series) deal( ...
    sqrt(mean((diff(series)/sqrt2).^2)), ...  % SD1
    sqrt(mean(((series(1:end-1) + series(2:end) - 2*mean(series))/sqrt2).^2)) ...  % SD2
);

% Rest phase
[SD1rest, SD2rest] = calculateSD(RR(phaseIndices.restStart:phaseIndices.phaseEnd1));

% Warm-up phase
[SD1warmUp, SD2warmUp] = calculateSD(RR(phaseIndices.warmUpStart:phaseIndices.phaseEnd2));

% Exercise phase
[SD1exercise, SD2exercise] = calculateSD(RR(phaseIndices.exerciseStart:phaseIndices.phaseEnd4));

% Recovery phase
[SD1recovery, SD2recovery] = calculateSD(RR(phaseIndices.recoveryStart:phaseIndices.phaseEnd6));

% Plot RR intervals vs. time
figure
plot(cleanedTimeData, cleanedRRIntervals, '.')
hold on

% Add lines to indicate phase transitions
line([7 7], [200 1200], 'Color', 'k')
line([9 9], [200 1200], 'Color', 'k')
line([20 20], [200 1200], 'Color', 'k')
line([0 35], [400 400], 'Color', 'r')
line([0 35], [600 600], 'Color', 'k')
line([0 35], [800 800], 'Color', 'k')
line([0 35], [1000 1000], 'Color', 'k')
line([1 1], [200 1200], 'Color', 'g')
line([6 6], [200 1200], 'Color', 'g')
line([14 14], [200 1200], 'Color', 'g')
line([19 19], [200 1200], 'Color', 'g')
line([25 25], [200 1200], 'Color', 'g')
line([30 30], [200 1200], 'Color', 'g')

% Annotate plot with mean values
text(2, 1200, num2str(stdRest))
text(2, 300, num2str(meanRest))
text(10, 1200, num2str(stdWarmUp))
text(10, 300, num2str(meanWarmUp))
text(22, 1200, num2str(stdExercise))
text(22, 300, num2str(meanExercise))
text(30, 1250, 'VFC')
text(30, 1200, '5 min')
text(30, 350, 'Mean RR')
text(30, 300, '5 min')

title(fileName)
xlabel('Time (minutes)')
ylabel('RR (ms)')

% Single Poincaré plot for all phases combined with color coding
figure
hold on

% Plot Poincaré plot for Rest phase
plot(RR(phaseIndices.restStart:phaseIndices.phaseEnd1-1), RR(phaseIndices.restStart+1:phaseIndices.phaseEnd1), 'b.')

% Plot Poincaré plot for Warm-up phase
plot(RR(phaseIndices.warmUpStart:phaseIndices.phaseEnd2-1), RR(phaseIndices.warmUpStart+1:phaseIndices.phaseEnd2), 'g.')

% Plot Poincaré plot for Exercise phase
plot(RR(phaseIndices.exerciseStart:phaseIndices.phaseEnd4-1), RR(phaseIndices.exerciseStart+1:phaseIndices.phaseEnd4), 'r.')

% Plot Poincaré plot for Recovery phase
plot(RR(phaseIndices.recoveryStart:phaseIndices.phaseEnd6-1), RR(phaseIndices.recoveryStart+1:phaseIndices.phaseEnd6), 'y.')

axis([300 1200 300 1200])
title('Poincaré Plot of RR Intervals by Phase')
xlabel('RR(n)')
ylabel('RR(n+1)')
legend('Rest', 'Warm-up', 'Exercise', 'Recovery')

% Display SD1 and SD2 for each phase
[SD1rest, SD2rest, SD1warmUp, SD2warmUp, SD1exercise, SD2exercise, SD1recovery, SD2recovery]
