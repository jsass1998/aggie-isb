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

function CourseSelectionPanel(props) {
  const [courses, setCourses] = useState([]);
  const [semester, setSemester] = useState('');

  const handleSemesterSelect = (event) => {
    setSemester(event.target.value);
  }

  const handleCourseSelect = (event, newValue) => {
    setCourses(newValue);
  }

  return (
    <div id='course-selection-panel'>
      <FormControl>
        <InputLabel id='semester-select-label'>Semester</InputLabel>
        <Select
          labelId='semester-select-label'
          value={semester}
          onChange={handleSemesterSelect}
        >
          <MenuItem value={'spring2021cstat'}>Spring 2021 - College Station</MenuItem>
          <MenuItem value={'spring2021cc'}>Spring 2021 - Corpus Cristi</MenuItem>
          <MenuItem value={'spring2021qatar'}>Spring 2021 - Qatar</MenuItem>
        </Select>
        <br/> <br/>
        <Autocomplete
          multiple
          autoComplete
          filterSelectedOptions
          options={props.courseList}
          getOptionLabel={(option) => option.course_id + ' - ' + option.title}
          style={{width: 500}}
          renderInput={(params) => <TextField {...params} label='Course Search' />}
          onChange={handleCourseSelect}
        />
      </FormControl>
      <br/> <br/>
      <Button variant='contained' color='primary' onClick={() => props.generateSchedules(courses)}>
        Find Schedules
      </Button>
    </div>
  );
}

function ScheduleListPanel(props) {
  const [expanded, setExpanded] = useState(true);

  const showOrHideCourseSelectionPanel = () => {
    if (expanded === false) {
      document.getElementById('side-panel').style.marginLeft = '0vw';
      document.getElementById('panel-expansion-button-icon').style.transform = 'rotate(180deg)';
    }
    else {
      document.getElementById('side-panel').style.marginLeft = '-31vw';
      document.getElementById('panel-expansion-button-icon').style.transform = 'rotate(0deg)';
    }
    setExpanded(!expanded);
  };

  return (
    <div id='schedule-list-panel'>
      <div id='panel-expansion-button' onClick={showOrHideCourseSelectionPanel}>
        <NavigateNextIcon id='panel-expansion-button-icon'/>
      </div>
    </div>
  );
}

class SidePanel extends Component {
  constructor(props) {
    super(props);
  }

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
              generateSchedules={this.props.generateSchedules}
            />
          </Grid>
          <Grid item xs={4}>
            <ScheduleListPanel />
          </Grid>
        </Grid>
      </div>
    );
  }
}

export default SidePanel;