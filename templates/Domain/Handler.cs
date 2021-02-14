using {{ProjectNamespace}}.Domain.Commands.Inputs.{{className}}s;
using {{ProjectNamespace}}.Domain.Commands.Inputs.Shared.Inputs;
using {{ProjectNamespace}}.Domain.Models;
using {{ProjectNamespace}}.Domain.Repositories;
using FluentValidation.Results;
using MediatR;
using NetDevPack.Messaging;
using System.Threading;
using System.Threading.Tasks;

namespace {{ProjectNamespace}}.Domain.Commands.Handlers
{
    public class {{className}}Handler : CommandHandler,
        IRequestHandler<Create{{className}}Command, ValidationResult>,
        IRequestHandler<Update{{className}}Command, ValidationResult>,
        IRequestHandler<DeleteCommand, ValidationResult>
    {

        private readonly I{{className}}Repository _{{className.lower()}}Repository;

        public {{className}}Handler(I{{className}}Repository {{className.lower()}}Repository)
        {
            _{{className.lower()}}Repository = {{className.lower()}}Repository;
        }

        public async Task<ValidationResult> Handle(Create{{className}}Command command, CancellationToken cancellationToken = default)
        {
            if (!command.IsValid()) return command.ValidationResult;

            //var {{className.lower()}} = new {{className}}(command.Name);

            _{{className.lower()}}Repository.Add({{className.lower()}});

            return await Commit(_{{className.lower()}}Repository.UnitOfWork);
        }

        public async Task<ValidationResult> Handle(Update{{className}}Command request, CancellationToken cancellationToken = default)
        {
            if (!command.IsValid()) return command.ValidationResult;

            var {{className.lower()}} = _{{className.lower()}}Repository.GetById(command.Id);

            _{{className.lower()}}Repository.Update({{className.lower()}});

            return await Commit(_{{className.lower()}}Repository.UnitOfWork);
        }

        public async Task<ValidationResult> Handle(DeleteCommand request, CancellationToken cancellationToken = default)
        {
            throw new System.NotImplementedException();
        }
    }
}
