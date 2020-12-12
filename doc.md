### Abstract Classes

* Parent
* Layout
* Widget
* State

```yaml
State : Text
    value : str
    id : str
    
    methods : 
        update : ( value, )
```

```yaml
State : List
    value : [  ]
    id : str
    
    methods : 
        update : ( value, )
```

```yaml
State : ListValue
    value : str
    id : str
    
    methods : 
        update : ( value, )
```

```yaml
Parent : Screen
    style : 
        height : int
        width : int
    _height : int
    _width : int
    _content : str

    methods:
        add : ( [ Layout | Widget ], )
        cache_geometry : ( , )
        cache_render : ( executer )
        update_state : ( state_id, value )
        render : executer
```

```yaml
Layout : HBox
    parent : Parent
    style : 
        height : int
        width : int
    _height : int
    _width : int
    _content : str

    methods:
        add : ( [ Layout | Widget ], )
        cache_geometry : ( , )
        cache_render : ( executer )
        update_state : ( state_id, value )
        render : executer
```

```yaml
Layout : VBox
    parent : Parent
    style : 
        height : int
        width : int
    _height : int
    _width : int
    _content : str

    methods:
        cache_geometry : ( , )
        cache_render : ( executer )
        update_state : ( state_id, value )
        render : executer
```

```yaml
Widget : Text
    parent : [ Parent | Layout ]
    style : 
        height : int
        width : int
    state : State[Text]
    _height : int
    _width : int
    _content : str

    methods:
        cache_geometry : ( , )
        cache_render : ( executer )
        update_state : ( state_id, value )
        render : executer
```