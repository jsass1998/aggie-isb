import React, { Component } from 'react';
import GoogleLogin from "react-google-login";
import { GOOGLE_CLIENT_ID } from "../utils/constants";

class TopBar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        const googleResponse = (response) => {
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
                      onSuccess={googleResponse}
                      onFailure={googleResponse}
                    />
                </div>
            </div>
        );
    }
}

export default TopBar;