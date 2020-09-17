import React, { Component } from 'react';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      secretMessage: "Click the button to see a secret message!",
    }
  }

  async getSecretMessage() {
    let data = await fetch('/api/')
    .then(res => res.json())
    .then(data => {
      return data;
    }).catch(err => console.log(err));
    console.log(JSON.parse(data.questions));
    this.setState({
      secretMessage: data.message,
    });
  }

  createQuestionObject() {
      let data = fetch('/api/create_question/')
      .catch(err => console.log(err));
  }

  render() {
    return (
      <div>
        <div style={{padding: '50px'}}>
          <h1>{this.state.secretMessage}</h1>
          <button onClick={this.getSecretMessage.bind(this)}>
            Click me!
          </button>
        </div>
        <br/>
        <div style={{padding: '50px'}}>
          <h1>Create a Question object</h1>
          <button onClick={this.createQuestionObject.bind(this)}>
            Create
          </button>
        </div>
      </div>
    );
  }
}

export default App;
