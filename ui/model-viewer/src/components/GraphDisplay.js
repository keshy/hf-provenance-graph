import logo from '../logo.svg';
import React from 'react';

function GraphDisplay(props) {

    return (
        <div>
         <div className="mt-3"></div>
         <div className="card">

              <h4 align='left'>Visualization</h4>
              <div className="card-body">
              {!props.searchQuery &&
                  <img src={logo} alt='No graph to display' />
              }
            </div>
        </div>
       </div>
    )
}

export default GraphDisplay;