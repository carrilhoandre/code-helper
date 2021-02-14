using {{ProjectNamespace}}.Domain.Commands.Inputs.{{plural}};
using FluentValidation;

namespace {{ProjectNamespace}}.Domain.Commands.Validations.{{plural}}
{
    public abstract class {{className}}Validation<T> : AbstractValidator<T> where T : {{className}}Command
    {
    }
}
