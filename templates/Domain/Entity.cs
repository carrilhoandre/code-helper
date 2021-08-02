using NetDevPack.Domain;
using System;

namespace {{ProjectNamespace}}.Domain.Models
{
    public {{EntityType.lower()}} {{EntityName}} : Entity, IAggregateRoot
    {
        public {{EntityName}}()
        {
        }

        protected {{EntityName}}() { }

        {% for item in EntityFields %}
        public {{item.Type}} {{item.Name}} { get; private set;}
        {% endfor %}
    }
}
