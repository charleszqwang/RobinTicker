import React, { Component } from 'react';
import Login from "./login"
import Verify from './verify'
import Ticker from './ticker'
import Loading from './loading'

class App extends Component {
    state = { 
        username: null,
        password: null,
        remember: false,
        device_token: null,
        auth_type: null,
        code: null,
        challenge_id: null,
        auth: 'loading',
        wrong: false,
        retries: 4,
      }
    
    async componentDidMount () {
        //check for saved login
        let urlArray = []
        urlArray.push('login', true)
        const response = await fetch(urlArray.join('/'));
        const data = await response.json();
        if(data['result'] === 'success'){
            this.setState({auth: 'success'})
        }
        else{
            this.setState({auth: 'login'})
        }
    }

    handleLogout = async (event) => {
        await fetch('logout');
        this.setState({auth: 'login'})
    }


    handleLogin = async (event) => {
        event.preventDefault()
        let urlArray = []
        urlArray.push('login', this.state.remember, this.state.username, this.state.password)
        const response = await fetch(urlArray.join('/'));
        const data = await response.json();
        if(data['result'] === 'challenge' || data['result'] === 'mfa'){
           this.setState({auth: 'verify', device_token: data['device_token']})
            if(data['result'] === 'mfa'){
                this.setState({auth_type: 'mfa'})
            }
            else
                this.setState({auth_type: 'challenge', challenge_id: data['challenge_id']})
            
        }
        else if(data['result'] === 'success' )
            this.setState({auth: 'success', wrong: false})
        else    
            this.setState({wrong: true, auth: 'login'})
    }

    handleInputChange = (event) => {
        event.preventDefault()
        this.setState({
            [event.target.name]: event.target.value
        })
    }

    handleVerify = async (event) => {
        event.preventDefault()
        let urlArray = []
        urlArray.push(
            'verify', 
            this.state.remember,
            this.state.username, 
            this.state.password,  
            this.state.device_token, 
            this.state.auth_type, 
            this.state.code, 
            this.state.challenge_id
        )
        const response = await fetch(urlArray.join('/'));
        const data = await response.json();
        if(data['access_token'])
            this.setState({auth: 'success', retries: 4})
        else if(data['error'])
            this.setState({retries: this.state.retries - 1})
        if(this.state.retries === 0)
            this.setState({retries: 4, auth: 'relogin'})
    }

    handleCheckboxChange = (event) => {
        this.setState({remember: event.target.checked})
    }

    render() { 
        if(this.state.auth === 'verify'){
            return (
                <>
                    <Verify
                        retries={this.state.retries}
                        onVerify={this.handleVerify}
                        onInputChange={this.handleInputChange}
                    />
                </>
            );
        }
        else if(this.state.auth === 'login' || this.state.auth === 'relogin') {
            return ( 
                <div className='center'>
                    <Login 
                        auth={this.state.auth}
                        wrong={this.state.wrong}
                        onChangeCheckbox={this.handleCheckboxChange}
                        onLogin={this.handleLogin}
                        onInputChange={this.handleInputChange}
                    />
                    {this.state.wrong ? (
                        <p className='error-msg gray'>Unable to log in with provided credentials.</p>
                        ) : null
                    }
                    {
                        this.state.auth === 'relogin' ? (
                            <p className='error-msg gray'>Exceeded allowed verification attempts. Sign in to continue.</p>
                        ) : null
                    }
                </div>
            );
        }
        else if(this.state.auth === 'loading'){
            return (
                <div className='center'>
                    <Loading/>
                </div>
            )
        }
        return (
            <Ticker 
                onLogout={this.handleLogout}
            />
        );
    }
}
 
export default App;