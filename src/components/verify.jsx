import React, { Component } from 'react';

class Verify extends Component {
    render() { 
        return ( 
            <div className='center'>
                <form className="form-signin" onSubmit={this.props.onVerify}>
                        <img className="mb-4" src="/feather.png" alt="" style={{width: "23vw", height: "29vh"}}/>
                        <p className='color'>A code has been sent to you via SMS.</p>
                        <input type="code" name="code" className="custom-input form-control" placeholder="Verification Code" required autoFocus onChange={this.props.onInputChange}/>
                        <button className="btn btn-default custom-btn">Verify</button>
                </form>
                {this.props.retries < 4 ? (
                    <p className='error-msg gray'>Incorrect Code, {this.props.retries} attempts left</p>
                ) : null} 
            </div>
         );
    }
}
 
export default Verify;