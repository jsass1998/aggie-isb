import React, { useState } from 'react';
import 'resize-observer-polyfill/dist/ResizeObserver.global';
import { TimeGridScheduler, classes } from '@remotelock/react-week-scheduler';
import '@remotelock/react-week-scheduler/index.css';

const rangeStrings = [
  ['2019-03-04 00:15', '2019-03-04 01:45'],
  ['2019-03-05 09:00', '2019-03-05 10:30'],
  ['2019-03-06 22:00', '2019-03-06 22:30'],
  ['2019-03-07 01:30', '2019-03-07 03:00'],
  ['2019-03-07 05:30', '2019-03-07 10:00'],
  ['2019-03-08 12:30', '2019-03-08 01:30'],
];

const testRange =  ['2019-03-09 22:00', '2019-03-09 23:59'];

const defaultSchedule = rangeStrings.map(range =>
  range.map(dateString => new Date(dateString)),
);

const newTimeBlock = testRange.map(dateString => new Date(dateString));

// TODO: Convert TimeGrid from a function to a react Component
function TimeGrid() {
  const [schedule, setSchedule] = useState(defaultSchedule);
  // console.log('schedule', schedule);
  // console.log('newTimeBlock', newTimeBlock);

  return (
    <div>
      <div className="time-grid">
        <TimeGridScheduler
          classes={classes}
          style={{ width: "100%", height: "100%" }}
          originDate={new Date('2019-03-04')}
          schedule={schedule}
          onChange={params => {console.log(params); setSchedule(params)}}
          visualGridVerticalPrecision={15} // show grid lines in 'x' minute intervals
          verticalPrecision={5} // Minute increments in which time blocks can be created
          cellClickPrecision={60} // Size of time block in minutes when user simply clicks once on grid
        />
      </div>
      <button onClick={() => setSchedule([...schedule, newTimeBlock])}>
        Add time
      </button>
    </div>
  );
}

export default TimeGrid;
