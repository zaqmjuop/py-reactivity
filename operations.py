from es6.Object import Object

TrackOpTypes = Object({
    "GET": 'get',
    "HAS": 'has',
    "ITERATE": 'iterate'
})

TriggerOpTypes = Object({
    "SET": 'set',
    "ADD": 'add',
    "DELETE": 'delete',
    "CLEAR": 'clear'
})

ReactiveFlags = Object({
    "SKIP": '__v_skip',
    "IS_REACTIVE": '__v_isReactive',
    "IS_READONLY": '__v_isReadonly',
    "IS_SHALLOW": '__v_isShallow',
    "RAW": '__v_raw'
})
