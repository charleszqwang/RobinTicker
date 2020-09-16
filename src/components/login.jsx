import React, { Component } from 'react';

class Login extends Component {
    render() { 
        return ( 
            <>
                <form className="form-signin" onSubmit={this.props.onLogin}>
                        <img className="mb-4" src="/feather.png" alt="" style={{width: "23vw", height: "29vh"}}/>
                        <input type="username" name="username" className="custom-input form-control" placeholder="Email address" required autoFocus onChange={this.props.onInputChange}/>
                        <input type="password" name="password" className="form-control custom-input" placeholder="Password" required onChange={this.props.onInputChange}/>
                        <button className="btn btn-default custom-btn">Sign In</button>
                        <table><tbody><tr><td>
                            <input type="checkbox" name="remember" onChange={this.props.onChangeCheckbox} />
                            <label className='custom-label gray'>Remember me</label>
                        </td></tr></tbody></table>
                </form>
            </>
         );
    }
}
 
export default Login;