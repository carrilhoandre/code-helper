using NetDevPack.Domain;
using System;

namespace {{projectNamespace}}.Domain.Models
{
    public {{classType.lower()}} {{className}} : Entity, IAggregateRoot
    {
        public {{className}}()
        {
        }

        protected {{className}}() { }

        {% for item in fields %}
        public {{item.Type}} {{item.Name}} {get; private set;}
        {% endfor %}
    }
}
