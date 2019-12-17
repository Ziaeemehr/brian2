{% extends 'common_group.cpp' %}
{# USES_VARIABLES { N } #}

{% block maincode %}
    {# t, not_refractory and lastspike are added as needed_variables in the
       Thresholder class, we cannot use the USES_VARIABLE mechanism
       conditionally.
       Same goes for "eventspace" (e.g. spikespace) which depends on the type of
       event #}

    //// MAIN CODE ////////////
    // scalar code
    const size_t _vectorisation_idx = 1;
    {{scalar_code|autoindent}}

    size_t _cpp_numevents = 0;

    {#  Get the name of the array that stores these events (e.g. the spikespace array) #}
    {% set _eventspace = get_array_name(eventspace_variable) %}

    for(size_t _idx=0; _idx<N; _idx++)
    {
        // vector code
        const size_t _vectorisation_idx = _idx;
        {{ super() }}
        if(_cond) {
            {{_eventspace}}[_cpp_numevents++] = _idx;
            {% if _uses_refractory %}
            {{not_refractory}}[_idx] = false;
            {{lastspike}}[_idx] = {{t}};
            {% endif %}
        }
    }
    {{_eventspace}}[N] = _cpp_numevents;
{% endblock %}
