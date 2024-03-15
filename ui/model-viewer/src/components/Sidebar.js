import React from 'react';
import useSearchTranslate from '../util/useSearchTranslate';

function Sidebar() {
    const {
        showQuery,
    } = useSearchTranslate();
    console.log('Show Query status' + showQuery)
    return (
    <div className="col-md-4">
    <div className="mt-3"></div>
    <div className="sidebar card">
    <h3 className="card-title">Conversations</h3>
    { showQuery && <div className="card-body">
        "hellow world"
      </div>
    }
    </div>
    </div>
    );
}
export default Sidebar