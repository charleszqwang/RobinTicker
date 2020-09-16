import React, { Component } from 'react';
import Counter from './counter'

class Counters extends Component {
    render() { 
        const {onReset, onDelete, onIncrement, counters} = this.props;
        return ( 
            <>
                <div>
                    <button 
                        onClick={onReset}
                        className="btn btn-sm m-2 btn-primary"
                    >
                        Reset
                    </button>
                </div>
                { counters.map(counter => 
                <Counter 
                    key={counter.id} 
                    counter={counter} 
                    onDelete={onDelete} 
                    onIncrement={onIncrement}
                />) }
            </>
         );
    }
}
 
export default Counters;