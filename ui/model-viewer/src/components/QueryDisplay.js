import React from 'react';

function QueryDisplay(props) {

    return (
        <div>
        <div className="mt-3"></div>
        { props.showQuery &&
          <div className="card mb-3">
            <h4 align='left'>Translated Query</h4>
            <div className="card-body">
              {props.translatedQuery}
              {/* query */}
            </div>
          </div>
        }
        </div>
    )
}

export default QueryDisplay;