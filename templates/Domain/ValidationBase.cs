using {{projectNamespace}}.Domain.Commands.Inputs.{{plural}};
using FluentValidation;

namespace {{projectNamespace}}.Domain.Commands.Validations.{{plural}}
{
    public abstract class {{className}}Validation<T> : AbstractValidator<T> where T : {{className}}Command
    {
    }
}
