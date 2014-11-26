<script>
// Import data.
window.dashboardData = {};
window.dashboardData.data_points = [];
{% for d in data_points %}
window.dashboardData.data_points.push({{d.json|safe}});{% endfor %}
window.dashboardData.milestones = [];
{% for m in milestones %}
window.dashboardData.milestones.push({{m.json|safe}});{% endfor %}
</script>