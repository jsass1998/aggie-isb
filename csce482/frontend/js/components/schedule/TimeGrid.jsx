import React, { useState } from 'react';
import 'resize-observer-polyfill/dist/ResizeObserver.global';
import { TimeGridScheduler, classes } from '@remotelock/react-week-scheduler';
import '@remotelock/react-week-scheduler/index.css';
import PopUpDialog from "../PopUpDialog";
import { create_schedule_tooltip } from "../../utils/constants";
import Button from "@material-ui/core/Button";
import { DialogTitle } from "@material-ui/core";
import Dialog from "@material-ui/core/Dialog";
import DialogContent from "@material-ui/core/DialogContent";
import DialogActions from "@material-ui/core/DialogActions";
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from "@material-ui/core/TextField";

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


function handleCheckChanged(checked) {
  localStorage.setItem('hideToolTips', checked ? '1' : '0');
}

function CourseSelectionPopUp(props) {
  const [courses, setCourses] = useState([]);

  const handleChange = (event, newValue) => {
    setCourses(newValue);
  }

  return (
    <Dialog open={props.active} aria-labelledby="form-dialog-title" onClose={props.onClose}>
      <DialogTitle id="form-dialog-title" className="popup-title">Create a New Schedule</DialogTitle>
      <DialogContent>
        <Autocomplete
          multiple
          autoComplete
          filterSelectedOptions
          options={props.courseList}
          getOptionLabel={(option) => option.course_id + ' - ' + option.title}
          style={{width: 500}}
          renderInput={(params) => <TextField {...params} label='Course Search' />}
          onChange={handleChange}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={() => {props.onClose(); props.generateSchedules(courses)}}>
          Generate
        </Button>
      </DialogActions>
    </Dialog>
  );
}

function TimeGrid(props) {
  const [schedule, setSchedule] = useState(defaultSchedule);
  const [hideToolTips, setHideToolTips] = useState(props.hideToolTips);
  const [showCourseSelection, setShowCourseSelection] = useState(false);

  const generateSchedules = (schedules) => {
    console.log('courses to add', schedules);
    // Here we would send a request to the backend to generate schedules
    // and handle the response.
  }

  return (
    <div>
      <PopUpDialog
        active={!hideToolTips}
        title='Create a Schedule'
        message={create_schedule_tooltip}
        onClose={() => setHideToolTips(true)}
        showCheckbox={true}
        checkboxText={"Don't show again"}
        handleCheckChanged={handleCheckChanged}
      />
      <CourseSelectionPopUp
        active={showCourseSelection}
        courseList={props.courseList}
        generateSchedules={generateSchedules}
        onClose={() => setShowCourseSelection(false)}
      />
      <div className="time-grid">
        <TimeGridScheduler
          classes={classes}
          style={{ width: "100%", height: "94.6%" }}
          originDate={new Date('2019-03-04')}
          schedule={schedule}
          onChange={params => {setSchedule(params)}}
          visualGridVerticalPrecision={30} // show grid lines in 'x' minute intervals
          verticalPrecision={5} // Minute increments in which time blocks can be created
          cellClickPrecision={60} // Size of time block in minutes when user simply clicks once on grid
        />
      </div>
      <Button
        id='add-course-button'
        variant='contained'
        color='primary'
        onClick={() => setShowCourseSelection(true)}
      >
        Add Courses
      </Button>
    </div>
  );
}

export default TimeGrid;
