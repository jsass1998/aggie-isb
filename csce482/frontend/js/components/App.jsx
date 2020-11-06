import React, {Component} from 'react';
import axios from 'axios';
import TopBar from "./TopBar";
import TimeGrid from "./schedule/TimeGrid";
import CircularProgress from "@material-ui/core/CircularProgress";
import ScheduleView from "./schedule/ScheduleView";

/*
  * <App/> is the root component for the schedule view page and will consist of the most
  * logic and complexity as it is where the user is expected to spend the majority of their
  * time interacting with the site.
 */

class App extends Component {
  constructor(props) {
    super(props);
    const { hideToolTips } = this.fetchLocalStorage();
    this.state = {
      hideToolTips: hideToolTips,
    }
  }

  fetchLocalStorage() {
    return {
      hideToolTips: Boolean(parseInt(localStorage.getItem('hideToolTips'))),
    };
  }

  render() {
    return(
      <div>
        <TopBar/>
        <ScheduleView
          hideToolTips={this.state.hideToolTips}
        />
      </div>
    );
  }
}

export default App;