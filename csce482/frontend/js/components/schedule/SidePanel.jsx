import React, {Component, useState} from 'react';
import Grid from "@material-ui/core/Grid";
import Autocomplete from "@material-ui/lab/Autocomplete";
import TextField from "@material-ui/core/TextField";
import {Button} from "@material-ui/core";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import NavigateNextIcon from '@material-ui/icons/NavigateNext';
import CardContent from "@material-ui/core/CardContent";
import Card from "@material-ui/core/Card";
import makeStyles from "@material-ui/core/styles/makeStyles";

function CourseSelectionPanel(props) {
  const [semester, setSemester] = useState('');
  const [selectedCourses, setSelectedCourses] = useState([]);

  const handleSemesterSelect = (event) => {
    if (event.target.value !== semester) {
      setSemester(event.target.value);
      props.onSemesterUpdated(event.target.value);
      props.fetchCourses(event.target.value);
      props.fetchuserSchedules(event.target.value);
    }
  }

  const handleCourseSelect = (event, newValue) => {
    props.onCourseListUpdated(newValue);
    setSelectedCourses(newValue);
  }

  const handleSubmit = () => {
    props.generateSchedules();
    if (selectedCourses.length > 0)
      props.showOrHideCourseSelectionPanel();
  }

  const semesters = props.semesterList.map(semester =>
    <MenuItem  key={`${semester.term}-${semester.location}`} value={`${semester.term}-${semester.location}`}>
      {`${semester.term} - ${semester.location}`}
    </MenuItem>
  );

  return (
    <div id='course-selection-panel'>
      <FormControl>
        <InputLabel id='semester-select-label'>Semester</InputLabel>
        <Select
          labelId='semester-select-label'
          value={semester}
          onChange={handleSemesterSelect}
        >
          {semesters}
        </Select>
        <br/> <br/>
        <Autocomplete
          disabled={!props.courseList.length}
          multiple
          autoComplete
          filterSelectedOptions
          options={props.courseList}
          getOptionLabel={(option) => option.course_id + ' - ' + option.title}
          renderInput={(params) => <TextField {...params} label='Course Search' />}
          onChange={handleCourseSelect}
        />
      </FormControl>
      <br/> <br/>
      <Button variant='contained' color='primary' onClick={handleSubmit}>
        Find Schedules
      </Button>
    </div>
  );
}

function ScheduleListPanel(props) {
  const useStyles = makeStyles({
    root: {
      margin: 10,
      height: 150,
    },
  });

  const Schedule = (props) => {
    const classes = useStyles();
    return(
      <Card className={classes.root} onClick={() => props.loadSchedule(props.schedule.activities)}>
        <CardContent className='schedule'>
          <div className='schedule-contents'>
            {/*<span>{props.schedule.campus}, {props.schedule.term} - {props.schedule.id}</span>*/}
            <span>Avg. Start: {props.schedule.avg_starttime}</span>
            <span>Avg. End: {props.schedule.avg_endtime}</span>
            <span>Avg. Day Length: {props.schedule.avg_day_length}</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  const schedules = props.scheduleList.map(schedule =>
    <Schedule
      key={schedule.id}
      schedule={schedule}
      loadSchedule={props.loadSchedule}
    />
  );

  const getScheduleListOrEmptyMessage = () => {
    if (props.scheduleList.length)
      return (
        <Grid
          container
          direction='column'
          justify='center'
          alignItems='stretch'
          style={{'flexWrap': 'nowrap', height: 'unset'}}
        >
          {schedules}
        </Grid>
      );
    else
      return (
        <div id='empty-schedule-message'>
          Expand to start adding courses
        </div>
      );
  };

  return (
    <div id='schedule-list-panel'>
      <div id='panel-expansion-button' onClick={props.showOrHideCourseSelectionPanel}>
        <NavigateNextIcon id='panel-expansion-button-icon'/>
      </div>
      <div id='schedule-list'>
        { getScheduleListOrEmptyMessage() }
      </div>
    </div>
  );
}

class SidePanel extends Component {
  constructor(props) {
    super(props);

    this.state = {
      expanded: false,
    };
  }

  showOrHideCourseSelectionPanel() {
    if (this.state.expanded === false) {
      document.getElementById('side-panel').style.marginLeft = '0vw';
      document.getElementById('panel-expansion-button-icon').style.transform = 'rotate(180deg)';
    }
    else {
      document.getElementById('side-panel').style.marginLeft = '-31vw';
      document.getElementById('panel-expansion-button-icon').style.transform = 'rotate(0deg)';
    }
    this.setState({
      expanded: !this.state.expanded,
    });
  };

  render() {
    return (
      <div id='side-panel' className='aisb-card'>
        <Grid
          container
          spacing={0}
          justify='center'
          alignItems='stretch'
          style={{height: '100%'}}
        >
          <Grid item xs={8}>
            <CourseSelectionPanel
              courseList={this.props.courseList}
              semesterList={this.props.semesterList}
              fetchCourses={this.props.fetchCourses}
              fetchuserSchedules={this.props.fetchUserSchedules}
              onSemesterUpdated={this.props.onSemesterUpdated}
              onCourseListUpdated={this.props.onCourseListUpdated}
              generateSchedules={this.props.generateSchedules}
              showOrHideCourseSelectionPanel={this.showOrHideCourseSelectionPanel.bind(this)}
            />
          </Grid>
          <Grid item xs={4}>
            <ScheduleListPanel
              scheduleList={this.props.scheduleList}
              loadSchedule={this.props.loadSchedule}
              showOrHideCourseSelectionPanel={this.showOrHideCourseSelectionPanel.bind(this)}
            />
          </Grid>
        </Grid>
      </div>
    );
  }
}

export default SidePanel;