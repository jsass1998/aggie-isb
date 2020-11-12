import React, { Component } from 'react';
import GoogleLogin from "react-google-login";
import axios from 'axios';
import { GOOGLE_CLIENT_ID } from "../utils/constants";

class TopBar extends Component {
    constructor(props) {
        super(props);
        let user = localStorage.getItem('user');
        this.state = {
          userName: user? user: 'Sign in',
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

      // Maybe unnecessary?
      if (res.data.key) {
        localStorage.setItem('api_key', res.data.key);
      }
      localStorage.setItem('user', token.profileObj.name);
      localStorage.setItem('email', token.profileObj.email);

      this.setState({
        userName: token.profileObj.name, // Kind of cheap, should try to fetch automatically if user has already signed in before
      });
      this.props.updateUserData({email: token.profileObj.email});
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