export default function Footer() {
  return (
    <footer className="border-t border-navy-600 py-8 px-6">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <img src="/assets/logo.svg" alt="MultiEntregas" className="h-6" />
        <p className="text-silver text-xs text-center">
          © {new Date().getFullYear()} MultiEntregas. Transporte internacional frigorífico.
        </p>
        <div className="flex gap-5 text-silver text-xs">
          <span className="hover:text-white cursor-pointer">Aviso legal</span>
          <span className="hover:text-white cursor-pointer">Privacidad</span>
        </div>
      </div>
    </footer>
  )
}
