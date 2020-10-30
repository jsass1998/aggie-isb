import React, { Component } from 'react';
import GoogleLogin from "react-google-login";
import axios from 'axios';
import { GOOGLE_CLIENT_ID } from "../utils/constants";

class TopBar extends Component {
    constructor(props) {
        super(props);
    }

    // TODO: Update Sign In button text with user name after authentication
    async signInUser(token) {
      let res = await axios.post(
        '/rest-auth/google/',
        {
          access_token: token.accessToken,
        }
      );
      console.log(res);
      return res.status;
    }

    render() {
        const googleErrorResponse = (response) => {
          console.log(response);
        }
        return(
            <div className='aisb-topbar aisb-card'>
                <h1>Aggie ISB</h1>
                {/* TODO: WIP - Finish user acct / sign in component */}
                <div id='sign-in'>
                    <GoogleLogin
                      clientId={GOOGLE_CLIENT_ID}
                      buttonText="Sign in"
                      onSuccess={this.signInUser}
                      onFailure={googleErrorResponse}
                    />
                </div>
            </div>
        );
    }
}

export default TopBar;