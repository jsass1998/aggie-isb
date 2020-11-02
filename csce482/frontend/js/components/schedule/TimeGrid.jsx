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
import makeStyles from "@material-ui/core/styles/makeStyles";
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

const testRange =  ['2019-03-09 22:00', '2019-03-09 23:59'];

const defaultSchedule = rangeStrings.map(range =>
  range.map(dateString => new Date(dateString)),
);

const newTimeBlock = testRange.map(dateString => new Date(dateString));

const convertToTimeBlock = rangeStrings => {
  return rangeStrings.map(range => range.map(dateString => new Date(dateString)),);
}

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}));

const availableCourses = [
    {
      title: 'CSCE 482-900',
      instance: [
        ['2019-03-04 09:00', '2019-03-04 12:00'], // Monday
        ['2019-03-06 09:00', '2019-03-06 12:00'], // Wednesday
      ]
    },
    {
      title: 'CSCE 436-500',
      instance: [
        ['2019-03-04 14:55', '2019-03-04 15:45'], // Monday
        ['2019-03-06 14:55', '2019-03-06 15:45'], // Wednesday
        ['2019-03-08 14:55', '2019-03-08 15:45'], // Friday
      ]
    },
    {
      title: 'MATH 407-500',
      instance: [
        ['2019-03-05 17:00', '2019-03-05 18:15'], // Tuesday
        ['2019-03-07 17:00', '2019-03-07 18:15'], // Thursday
      ]
    },
  ];

function handleCheckChanged() {
  console.log('checked');
}

function CourseSelectionPopUp(props) {
  const classes = useStyles();
  const [courses, setCourses] = useState([]);

  const handleChange = (event) => {
    availableCourses.forEach(course => {
      if (course.title === event.target.innerText) {
        setCourses([...courses, course.instance]);
      }
    });
  }

  return (
    <Dialog open={props.active} aria-labelledby="form-dialog-title" onClose={props.onClose}>
      <DialogTitle id="form-dialog-title" className="popup-title">Create a New Schedule</DialogTitle>
      <DialogContent>
        <Autocomplete
          multiple
          filterSelectedOptions
          options={availableCourses}
          getOptionLabel={(option) => option.title}
          style={{width: 300}}
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
  const [showToolTips, setShowToolTips] = useState(props.showToolTips);
  const [showCourseSelection, setShowCourseSelection] = useState(false);

  const generateSchedules = (schedules) => {
    let newEvents = schedule;
    schedules.forEach(course => {
      let instances = convertToTimeBlock(course);
      instances.forEach(instance => {
        newEvents.push(instance);
      });
    });
    setSchedule(newEvents);
  }

  return (
    <div>
      <PopUpDialog
        active={showToolTips}
        title='Create a Schedule'
        message={create_schedule_tooltip}
        onClose={() => setShowToolTips(false)}
        handleCheckChanged={handleCheckChanged}
      />
      <CourseSelectionPopUp
        active={showCourseSelection}
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
