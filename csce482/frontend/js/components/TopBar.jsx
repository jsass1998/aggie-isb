import React, { Component } from 'react';
import GoogleLogin from "react-google-login";
import axios from 'axios';
import { GOOGLE_CLIENT_ID } from "../utils/constants";

class TopBar extends Component {
    constructor(props) {
        super(props);
        this.state = {
          userName: 'Sign in'
        };
    }

    // TODO: Update Sign In button text with user name after authentication
    async signInUser(token) {
      let res = await axios.post(
        '/rest-auth/google/',
        {
          access_token: token.accessToken,
        }
      );

      if (res.data.key)
        localStorage.setItem('api_key', res.data.key);

      this.setState({
        userName: token.profileObj.name, // Kind of cheap, should try to fetch automatically if user has already signed in before
      });
    }

    render() {
        const googleErrorResponse = (response) => {
          console.error(response);
        }
        return(
            <div className='aisb-topbar aisb-card'>
                <h1>Aggie ISB</h1>
                {/* TODO: WIP - Finish user acct / sign in component */}
                <div id='sign-in'>
                    <GoogleLogin
                      clientId={GOOGLE_CLIENT_ID}
                      buttonText={this.state.userName}
                      onSuccess={this.signInUser.bind(this)}
                      onFailure={googleErrorResponse}
                    />
                </div>
            </div>
        );
    }
}

export default TopBar;