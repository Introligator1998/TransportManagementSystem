
{% block content %}

<link rel = "stylesheet" href ="../static/dtest/jquery.datetimepicker.min.css">
<script src = ../static/dtest/jquery.js"></script>
<script src = "../static/dtest/jquery.datetimepicker.full.js"></script>

<input id = "datetime">

<script>
    $("#datetime").datetimepicker();
</script>

{% endblock content %}