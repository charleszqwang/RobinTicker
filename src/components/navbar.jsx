import React, { Component } from 'react';

class Navbar extends Component {
    render() { 
        const {equity, changePercent, changeDollar, positive} = this.props.state
        return ( 
            <nav className={"navbar navbar-light " + (positive ? 'up-green' : 'down-red')}>
                <div className='numbers'>
                    <p className='balance m-0'>{equity}</p>
                    <p className='change m-0'>{changeDollar} ({changePercent}%)</p>
                </div>
                <div className='navbar-icon-div m-3'>
                    <img className='navbar-icon' src='/logout.ico' alt='logout' onClick={this.props.onLogout}/>
                    <img className='navbar-icon' src='/refresh.ico' alt='refresh' onClick={this.props.onRefresh}/>
                </div>
            </nav>
        );
    }
}
 
export default Navbar;