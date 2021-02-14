namespace {{ProjectNamespace}}.Domain.Enums
{
    public enum {{className}}
    {
        {% for item in values %}
        {{item.Name}} = {{item.Value}},
        {% endfor %}
    }
}
