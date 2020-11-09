import React, {Component} from 'react';
import TopBar from "./TopBar";
import ScheduleView from "./schedule/ScheduleView";

/*
  * <App/> is the root component for the schedule view page and will consist of the most
  * logic and complexity as it is where the user is expected to spend the majority of their
  * time interacting with the site.
 */

class App extends Component {
  constructor(props) {
    super(props);
    const { hideToolTips, userEmail } = this.fetchLocalStorage();
    this.state = {
      hideToolTips: hideToolTips,
      userEmail: userEmail,
    }
  }

  fetchLocalStorage() {
    return {
      hideToolTips: Boolean(parseInt(localStorage.getItem('hideToolTips'))),
      userEmail: localStorage.getItem('email'),
    };
  }

  updateUserData(newData) {
    this.setState({
      userEmail: newData.email,
    });
  }

  render() {
    return(
      <div>
        <TopBar
          updateUserData={this.updateUserData.bind(this)}
        />
        <ScheduleView
          userEmail={this.state.userEmail}
          hideToolTips={this.state.hideToolTips}
        />
      </div>
    );
  }
}

export default App;