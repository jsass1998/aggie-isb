import React, {useContext} from 'react';
import 'resize-observer-polyfill/dist/ResizeObserver.global';
import {classes, TimeGridScheduler} from '@remotelock/react-week-scheduler';
import '@remotelock/react-week-scheduler/index.css';
import {ScheduleContext} from "./ScheduleContext";

/*
* Sun   - 2019-03-03
* Mon   - 2019-03-04
* Tues  - 2019-03-05
* Wed   - 2019-03-06
* Thurs - 2019-03-07
* Fri   - 2019-03-08
* Sat   - 2019-03-09
 */
const rangeStrings = [
  // ['2019-03-04 00:15', '2019-03-04 01:45'],
  // ['2019-03-05 09:00', '2019-03-05 10:30'],
  // ['2019-03-06 22:00', '2019-03-06 22:30'],
  // ['2019-03-07 01:30', '2019-03-07 03:00'],
  // ['2019-03-07 05:30', '2019-03-07 10:00'],
  // ['2019-03-08 12:30', '2019-03-08 01:30'],
];

const defaultSchedule = rangeStrings.map(range =>
  range.map(dateString => new Date(dateString)),
);

const convertToTimeBlock = rangeStrings => {
  return rangeStrings.map(range => range.map(dateString => new Date(dateString)),);
}

const EventContent = function CustomEventContent(props) {
  const context = useContext(ScheduleContext);
  return (
    <div className='event-content'>
      {context(props.dateRange)}
    </div>
  )
}

function TimeGrid(props) {
  return (
    <div className='time-grid'>
      <TimeGridScheduler
        classes={classes}
        style={{ width: "100%", height: "94.6%" }}
        originDate={new Date('2019-03-04')}
        schedule={props.schedule}
        onChange={props.handleGridChange}
        eventContentComponent={EventContent}
        visualGridVerticalPrecision={30} // show grid lines in 'x' minute intervals
        verticalPrecision={5} // Minute increments in which time blocks can be created
        cellClickPrecision={60} // Size of time block in minutes when user simply clicks once on grid
      />
    </div>
  );
}

export default TimeGrid;
