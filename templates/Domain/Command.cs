using {{ProjectNamespace}}.Domain.Commands.Validations.{{plural}};

namespace {{ProjectNamespace}}.Domain.Commands.Inputs.{{plural}}
{
    public class {{type}}{{className}}Command : {{className}}Command
    {
        public override bool IsValid()
        {
            ValidationResult = new Create{{className}}Validation().Validate(this);
            return ValidationResult.IsValid;
        }
    }
}
