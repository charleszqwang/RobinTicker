import React, { Component } from 'react';
import Navbar from './navbar'

class Ticker extends Component {
    state = { 
        equity: null,
        changeDollar: null,
        changePercent: null,
        positive: null
    }

    async componentDidMount(){
        await this.updateBalance()
    }

    formatDollar(rawNum, plusSign=false){
        let num = parseFloat(rawNum)
        let prefix = '$'
        if(num < 0){
            prefix = '-' + prefix
            num *= -1
        }
        else if(plusSign){
            prefix = '+' + prefix
        }
        return prefix + num.toLocaleString(undefined, {maximumFractionDigits:2})
    }

    formatPercent(rawPercent){
        return rawPercent >= 0 ? '+' + parseFloat(rawPercent).toLocaleString(undefined, {maximumFractionDigits:1})
            : parseFloat(rawPercent).toLocaleString(undefined, {maximumFractionDigits:1})
    }

    async updateBalance() {
        const response = await fetch('/balance');
        const data = await response.json();

        const changeDollar = data['equity'] - data['adjusted_equity_previous_close']
        const changePercent = (changeDollar/data['adjusted_equity_previous_close'])*100
        this.setState({
            equity: this.formatDollar(data['equity']) ,
            changeDollar: this.formatDollar(changeDollar, this.plusSign=true) ,
            changePercent: this.formatPercent(changePercent),
            positive: changePercent >= 0
        })
    }

    handleRefresh = async (event) => {
        await this.updateBalance()
    }


    render() { 
        return ( 
            <>
                <Navbar
                    onRefresh={this.handleRefresh}
                    onLogout={this.props.onLogout}
                    state={this.state}
                />

            </>
         );
    }
}
 
export default Ticker;