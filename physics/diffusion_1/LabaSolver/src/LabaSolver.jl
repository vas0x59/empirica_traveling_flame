

__precompile__()
module LabaSolver
    using Gridap
    using GridapGmsh
  export run;
  function __init__()
    println("Hello, World")
  end
  function run(workdir::String, p::Float64)
    model = GmshDiscreteModel(workdir * "/mesh.msh")

    d_tags = Vector{String}()
    n_tags = Vector{String}()

    for t in model.face_labeling.tag_to_name 
        v = split(t, " ")
        if v[1] == "b"
            if v[3] == "D"
                push!(d_tags, t)
            end
            if v[3] == "N"
                push!(n_tags, t)
            end
        end

    end
    println(d_tags)
    println(n_tags)

    order = 1
    reffe = ReferenceFE(lagrangian,Float64,order)
    gs = []
    for t in d_tags
        # V0 = TestFESpace(model,reffe,dirichlet_tags=t)
        # push!(test_fields, V0)
        v = split(t, " ")
        volt =  parse(Float64, v[4])
        push!(gs, x -> volt)
    end

    V0 = TestFESpace(model,reffe,dirichlet_tags=d_tags)
    U = TrialFESpace(V0,gs)

    degree = 2
    Ω = Triangulation(model)
    dΩ = Measure(Ω,degree)

    Γ = BoundaryTriangulation(model,tags=n_tags)
    dΓ = Measure(Γ,degree)
    

    f(x) = 0.0
    h(x) = 0.0
    vel = VectorValue(-p,0.0)
    a(u,v) = ∫( ∇(v)⋅∇(u) )*dΩ  + ∫(vel ⋅ ∇(u) * v)*dΩ
    b(v) = ∫( v*f )*dΩ + ∫( v*h )*dΓ

    op = AffineFEOperator(a,b,U,V0)


    ls = LUSolver()
    solver = LinearFESolver(ls)

    println("runing solver")
    uh = solve(solver,op)
    println("writing results")

    writevtk(Ω,workdir * "/results",cellfields=["uh"=>uh])
  end
  precompile(run, (String,))
end
